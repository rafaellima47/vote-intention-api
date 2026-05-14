from __future__ import annotations

from fastapi import APIRouter, status

from app.votes.repository import VoteRepository
from app.votes.schemas import VoteCreateRequest, VoteCreateResponse
from app.votes.service import VoteService

router = APIRouter(prefix="/votos", tags=["votos"])


@router.post("", response_model=VoteCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_vote(payload: VoteCreateRequest) -> VoteCreateResponse:
    service = VoteService(repository=VoteRepository())
    await service.register_vote(cpf=payload.cpf, candidate_id=payload.candidato_id)
    return VoteCreateResponse(mensagem="Voto registrado com sucesso")
