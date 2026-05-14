from __future__ import annotations

from app.candidates.data import candidate_list
from app.candidates.schemas import CandidateResponse


class CandidateService:
    async def list_candidates(self) -> list[CandidateResponse]:
        return [CandidateResponse.model_validate(candidate) for candidate in candidate_list]
