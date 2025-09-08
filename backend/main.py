from __future__ import annotations

from .app.auth import get_current_user
from .app.database import Base, engine, get_session, create_database

import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from .app.auth import get_current_user
from .app.database import Base, engine, get_session
from .app.models import User
from .app.routers import applications as applications_router
from .app.routers import auth as auth_router
from .app.routers import companies as companies_router
from .app.routers import students as students_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_database()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Internship Portal API", lifespan=lifespan)

origins = [
    os.getenv("FRONTEND_ORIGIN", "http://localhost:5500"),
    "http://127.0.0.1:5500",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Wire /auth/me dependency to use get_current_user
@auth_router.router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return current_user


app.include_router(auth_router.router, prefix="/api")
app.include_router(companies_router.router, prefix="/api")
app.include_router(students_router.router, prefix="/api")
app.include_router(applications_router.router, prefix="/api")


@app.get("/api/health")
async def health(session: AsyncSession = Depends(get_session)):
    return {"status": "ok"}

