from __future__ import annotations

from fastapi import status


class VoteDomainError(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Erro ao processar voto"

    def __init__(self, detail: str | None = None) -> None:
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class InvalidCpfError(VoteDomainError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "CPF deve conter exatamente 11 dígitos numéricos"


class CandidateNotFoundError(VoteDomainError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "candidato_id inválido"


class CpfAlreadyVotedError(VoteDomainError):
    status_code = status.HTTP_409_CONFLICT
    detail = "CPF já registrou um voto"
