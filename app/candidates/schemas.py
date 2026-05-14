from __future__ import annotations

from pydantic import BaseModel


class CandidateResponse(BaseModel):
    id: int
    nome: str
    numero: int
