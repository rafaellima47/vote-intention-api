from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None
_database_url_cache: str | None = None


def _get_default_database_path() -> str:
    return str(Path(__file__).resolve().parent.parent / "votes.db")


def get_database_url() -> str:
    configured_database_url = os.getenv("DATABASE_URL")
    if configured_database_url:
        return configured_database_url

    configured_database_path = os.getenv("DATABASE_PATH", _get_default_database_path())
    return f"sqlite+aiosqlite:///{configured_database_path}"


def _get_session_factory() -> async_sessionmaker[AsyncSession]:
    global _engine, _session_factory, _database_url_cache

    current_database_url = get_database_url()
    if _engine is None or _session_factory is None or _database_url_cache != current_database_url:
        _engine = create_async_engine(current_database_url, future=True)
        _session_factory = async_sessionmaker(_engine, expire_on_commit=False)
        _database_url_cache = current_database_url

    return _session_factory


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    session_factory = _get_session_factory()
    async with session_factory() as session:
        yield session


async def init_database() -> None:
    from app.votes.model import Base

    _get_session_factory()
    if _engine is None:
        raise RuntimeError("Database engine is not initialized")

    engine = _engine
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
