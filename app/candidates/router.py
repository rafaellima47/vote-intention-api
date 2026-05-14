from __future__ import annotations

from fastapi import APIRouter

from app.candidates.schemas import CandidateResponse
from app.candidates.service import CandidateService

router = APIRouter(prefix="/candidatos", tags=["candidatos"])


@router.get("", response_model=list[CandidateResponse])
async def list_candidates() -> list[CandidateResponse]:
    service = CandidateService()
    return await service.list_candidates()
