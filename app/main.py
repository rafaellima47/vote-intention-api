from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.candidates.router import router as candidates_router
from app.database import init_database
from app.results.router import router as results_router
from app.votes.router import router as votes_router

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await init_database()
    yield


app = FastAPI(
    title="API de Intenções de Voto",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(candidates_router)
app.include_router(votes_router)
app.include_router(results_router)
