from __future__ import annotations

from typing import AsyncGenerator
import os
import asyncio
import asyncpg
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


async def create_database():
    try:
        conn = await asyncpg.connect(
            user='postgres',
            password='password',
            database='postgres',
            host='localhost'
        )
        print("✅ Database connection is successful")
        await conn.execute('CREATE DATABASE internship')
        await conn.close()
    except asyncpg.exceptions.DuplicateDatabaseError:
        print("✅ Database already exists")
        pass

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/internship")


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

async def test_connection():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Database connection is successful")
    except Exception as e:
        print("❌ Database connection failed:", e)

if __name__ == "__main__":
    asyncio.run(test_connection())