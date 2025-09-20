from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from pydantic import BaseModel, EmailStr, field_validator
from .utils import validate_password_strength

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    role: str = Field(pattern="^(student|company)$")
    recaptcha: str | None = None  

    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        return validate_password_strength(v)

class UserBase(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserBase

    class Config:
        from_attributes = True


class CompanyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    logo_url: Optional[str] = None


class CompanyOut(CompanyCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class StudentCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    education: Optional[str] = None
    skills: Optional[str] = None
    resume_url: Optional[str] = None
    phone: Optional[str] = None


class StudentUpdate(StudentCreate):
    pass


class StudentOut(StudentCreate):
    id: int
    first_name: str
    user_id: int

    class Config:
        from_attributes = True


class InternshipCreate(BaseModel):
    title: str
    description: str
    requirements: Optional[str] = None
    stipend: Optional[str] = None
    duration: Optional[str] = None
    location: Optional[str] = None
    deadline: Optional[datetime] = None
    is_active: bool = True


class InternshipOut(InternshipCreate):
    id: int
    company_id: int
    company: CompanyCreate

    class Config:
        from_attributes = True


class ApplicationCreate(BaseModel):
    internship_id: int
    cover_letter: Optional[str] = None


class ApplicationOut(BaseModel):
    id: int
    student_id: int
    internship_id: int
    cover_letter: Optional[str]
    status: str
    applied_at: datetime

    class Config:
        from_attributes = True
