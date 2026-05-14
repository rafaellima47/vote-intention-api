from __future__ import annotations

from fastapi import APIRouter

from app.results.schemas import ResultsResponse
from app.results.service import ResultsService

router = APIRouter(prefix="/resultados", tags=["resultados"])


@router.get("", response_model=ResultsResponse)
async def get_results() -> ResultsResponse:
    service = ResultsService()
    return await service.get_results()
