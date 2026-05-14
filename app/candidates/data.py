from __future__ import annotations

from typing import TypedDict


class CandidateDict(TypedDict):
    id: int
    nome: str
    numero: int


candidate_list: list[CandidateDict] = [
    {"id": 1, "nome": "Maria Silva", "numero": 13},
    {"id": 2, "nome": "João Souza", "numero": 45},
]


candidate_ids: set[int] = {candidate["id"] for candidate in candidate_list}
