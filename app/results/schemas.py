from __future__ import annotations

from pydantic import BaseModel


class CandidateResultResponse(BaseModel):
    id: int
    nome: str
    votos: int
    percentual: float


class ResultsResponse(BaseModel):
    total_votos: int
    candidatos: list[CandidateResultResponse]
