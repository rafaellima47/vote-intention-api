from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.candidates.router import router as candidates_router
from app.database import init_database
from app.results.router import router as results_router
from app.votes.router import router as votes_router
from app.votes.errors import VoteDomainError

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await init_database()
    yield


app = FastAPI(
    title="API de Intenções de Voto",
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(VoteDomainError)
async def vote_domain_error_handler(_: Request, error: VoteDomainError) -> JSONResponse:
    return JSONResponse(
        status_code=error.status_code,
        content={"detail": error.detail},
    )


app.include_router(candidates_router)
app.include_router(votes_router)
app.include_router(results_router)
