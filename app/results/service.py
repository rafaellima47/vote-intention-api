from __future__ import annotations

from sqlalchemy import func, select

from app.candidates.data import candidate_list
from app.database import get_session
from app.results.schemas import CandidateResultResponse, ResultsResponse
from app.votes.model import Vote


class ResultsService:
    async def get_results(self) -> ResultsResponse:
        vote_counts = await self._get_vote_counts()
        total_votes = sum(vote_counts.values())

        candidate_results: list[CandidateResultResponse] = []
        for candidate in candidate_list:
            candidate_votes = vote_counts.get(candidate["id"], 0)
            percentage = round((candidate_votes / total_votes) * 100, 2) if total_votes > 0 else 0.0
            candidate_results.append(
                CandidateResultResponse(
                    id=candidate["id"],
                    nome=candidate["nome"],
                    votos=candidate_votes,
                    percentual=percentage,
                )
            )

        return ResultsResponse(total_votos=total_votes, candidatos=candidate_results)

    async def _get_vote_counts(self) -> dict[int, int]:
        async with get_session() as session:
            statement = select(Vote.candidate_id, func.count(Vote.id)).group_by(Vote.candidate_id)
            rows = await session.execute(statement)
            result_rows = rows.all()

        return {
            int(candidate_id): int(total_votes)
            for candidate_id, total_votes in result_rows
        }
