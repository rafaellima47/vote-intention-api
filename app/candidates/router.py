from __future__ import annotations

from fastapi import APIRouter

from app.candidates.data import candidate_list
from app.candidates.schemas import CandidateResponse

router = APIRouter(prefix="/candidatos", tags=["candidatos"])


@router.get("", response_model=list[CandidateResponse])
async def list_candidates() -> list[CandidateResponse]:
    return [CandidateResponse.model_validate(candidate) for candidate in candidate_list]
