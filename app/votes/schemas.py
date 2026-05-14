from __future__ import annotations

from pydantic import BaseModel


class VoteCreateRequest(BaseModel):
    cpf: str
    candidato_id: int


class VoteCreateResponse(BaseModel):
    mensagem: str
