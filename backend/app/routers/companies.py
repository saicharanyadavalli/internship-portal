from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from .. import schemas
from ..auth import require_role
from ..database import get_session
from ..models import Company, Internship, User, Student, Application


router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("/profile", response_model=schemas.CompanyOut)
async def upsert_company_profile(
    data: schemas.CompanyCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(require_role("company"))],
):
    result = await session.execute(select(Company).where(Company.user_id == current_user.id))
    company = result.scalar_one_or_none()
    if company is None:
        company = Company(user_id=current_user.id, **data.model_dump())
        session.add(company)
    else:
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(company, k, v)
    await session.commit()
    await session.refresh(company)
    return company


@router.post("/internships", response_model=schemas.InternshipOut)
async def create_internship(
    data: schemas.InternshipCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(require_role("company"))],
):
    result = await session.execute(select(Company).where(Company.user_id == current_user.id))
    company = result.scalar_one_or_none()
    if company is None:
        raise HTTPException(status_code=400, detail="Company profile not found")
    internship = Internship(company_id=company.id, **data.model_dump())
    session.add(internship)
    await session.commit()
    await session.refresh(internship)
    return internship


@router.get("/internships", response_model=List[schemas.InternshipOut])
async def list_internships(session: Annotated[AsyncSession, Depends(get_session)]):
    result = await session.execute(select(Internship))
    return list(result.scalars())

@router.get("/applicants", response_model=List[schemas.ApplicationOut])
async def get_all_applicants(
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(require_role("company"))]
):
    # Get the company
    result = await session.execute(select(Company).where(Company.user_id == current_user.id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company profile not found")

    # Get all applications for the company's internships and load student info
    result = await session.execute(
        select(Application)
        .join(Internship)
        .where(Internship.company_id == company.id)
        .options(selectinload(Application.student).selectinload(Student.user))
    )
    applications = result.scalars().all()

    # Prepare list of applicants
    applicants_list = []
    for app in applications:
        student = app.student
        applicants_list.append({
            "id": student.id,
            "full_name": student.full_name,
            "email": student.user.email,
            "resume_url": student.resume_url,
            "applied_internship_id": app.internship_id,
            "cover_letter": app.cover_letter,
            "status": app.status,
            "applied_at": app.applied_at
        })

    return applicants_list

