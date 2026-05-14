from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.votes.repository import VoteRepository
from app.votes.schemas import VoteCreateRequest, VoteCreateResponse
from app.votes.service import (
    CandidateNotFoundError,
    CpfAlreadyVotedError,
    InvalidCpfError,
    VoteService,
)

router = APIRouter(prefix="/votos", tags=["votos"])


@router.post("", response_model=VoteCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_vote(payload: VoteCreateRequest) -> VoteCreateResponse:
    service = VoteService(repository=VoteRepository())

    try:
        await service.register_vote(cpf=payload.cpf, candidate_id=payload.candidato_id)
    except InvalidCpfError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CPF deve conter exatamente 11 dígitos numéricos") from error
    except CandidateNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="candidato_id inválido") from error
    except CpfAlreadyVotedError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CPF já registrou um voto") from error

    return VoteCreateResponse(mensagem="Voto registrado com sucesso")
