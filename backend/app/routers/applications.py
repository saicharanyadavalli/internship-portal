from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from ..auth import require_role
from ..database import get_session
from ..models import Application, Company, Internship, User

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("/company", response_model=List[schemas.ApplicationOut])
async def list_company_applications(
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(require_role("company"))],
):
    company = (await session.execute(select(Company).where(Company.user_id == current_user.id))).scalar_one()
    result = await session.execute(
        select(Application).join(Internship).where(Internship.company_id == company.id)
    )
    return list(result.scalars())

