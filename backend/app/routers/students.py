from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from ..auth import require_role
from ..database import get_session
from ..models import Application, Internship, Student, User
from ..utils import save_upload

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/addprofile", response_model=schemas.StudentOut)
async def upsert_student_profile(
    data: schemas.StudentCreate,
    file: UploadFile | None = File(None),
    session: Annotated[AsyncSession, Depends(get_session)] = None,
    current_user: Annotated[User, Depends(require_role("student"))] = None,
):
    result = await session.execute(select(Student).where(Student.user_id == current_user.id))
    student = result.scalar_one_or_none()

    # If resume file is uploaded, send to Cloudinary and get URL
    resume_url = None
    if file:
        content = await file.read()
        try:
            resume_url = save_upload(content, file.filename)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    if student is None:
        create_data = data.model_dump()
        if resume_url:
            create_data["resume_url"] = resume_url
        student = Student(user_id=current_user.id, **create_data)
        session.add(student)
    else:
        update_data = data.model_dump(exclude_unset=True)
        if resume_url:
            update_data["resume_url"] = resume_url
        for k, v in update_data.items():
            setattr(student, k, v)

    await session.commit()
    await session.refresh(student)
    return student

@router.get("/me", response_model=schemas.StudentOut)
async def get_my_profile(
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(require_role("student"))],
):
    result = await session.execute(select(Student).where(Student.user_id == current_user.id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Profile not found")
    return student

@router.put("/me", response_model=schemas.StudentOut)
async def update_my_profile(
    data: schemas.StudentUpdate,
    file: UploadFile | None = File(None),
    session: Annotated[AsyncSession, Depends(get_session)] = None,
    current_user: Annotated[User, Depends(require_role("student"))] = None,
):
    result = await session.execute(select(Student).where(Student.user_id == current_user.id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Profile not found")

    update_data = data.model_dump(exclude_unset=True)

    # Handle resume upload if file is provided
    if file:
        content = await file.read()
        try:
            resume_url = save_upload(content, file.filename)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        update_data["resume_url"] = resume_url

    # Update all fields from update_data
    for k, v in update_data.items():
        setattr(student, k, v)

    await session.commit()
    await session.refresh(student)
    return student

@router.post("/applications", response_model=schemas.ApplicationOut)
async def apply_to_internship(
    data: schemas.ApplicationCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(require_role("student"))],
):
    internship = await session.get(Internship, data.internship_id)
    if internship is None:
        raise HTTPException(status_code=404, detail="Internship not found")

    result = await session.execute(select(Student).where(Student.user_id == current_user.id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=400, detail="Create student profile first")

    application = Application(
        student_id=student.id,
        internship_id=internship.id,
        cover_letter=data.cover_letter,
    )
    session.add(application)
    await session.commit()
    await session.refresh(application)
    return application



@router.get("/applications", response_model=List[schemas.ApplicationOut])
async def list_my_applications(
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(require_role("student"))],
):
    result = await session.execute(
        select(Application).join(Student).where(Student.user_id == current_user.id)
    )
    return list(result.scalars())

