from __future__ import annotations

import re

from app.candidates.data import candidate_ids
from app.votes.errors import CandidateNotFoundError, CpfAlreadyVotedError, InvalidCpfError
from app.votes.repository import DuplicateCpfVoteError, VoteRepository


class VoteService:
    def __init__(self, repository: VoteRepository) -> None:
        self.repository = repository

    async def register_vote(self, cpf: str, candidate_id: int) -> None:
        self._validate_cpf(cpf)
        self._validate_candidate(candidate_id)

        if await self.repository.cpf_already_voted(cpf):
            raise CpfAlreadyVotedError

        try:
            await self.repository.create_vote(cpf, candidate_id)
        except DuplicateCpfVoteError as error:
            raise CpfAlreadyVotedError from error

    @staticmethod
    def _validate_cpf(cpf: str) -> None:
        if not re.fullmatch(r"\d{11}", cpf):
            raise InvalidCpfError

    @staticmethod
    def _validate_candidate(candidate_id: int) -> None:
        if candidate_id not in candidate_ids:
            raise CandidateNotFoundError
