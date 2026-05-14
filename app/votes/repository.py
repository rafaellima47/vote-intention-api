from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database import get_session
from app.votes.model import Vote


class VoteRepository:
    async def cpf_already_voted(self, cpf: str) -> bool:
        async with get_session() as session:
            statement = select(Vote.id).where(Vote.cpf == cpf).limit(1)
            row = await session.execute(statement)
            return row.scalar_one_or_none() is not None

    async def create_vote(self, cpf: str, candidate_id: int) -> None:
        async with get_session() as session:
            session.add(Vote(cpf=cpf, candidate_id=candidate_id))
            try:
                await session.commit()
            except IntegrityError as error:
                await session.rollback()
                if "UNIQUE constraint failed: votes.cpf" in str(error.orig):
                    raise DuplicateCpfVoteError from error
                raise


class DuplicateCpfVoteError(Exception):
    pass
