from typing import Optional, List

from sqlalchemy import select, delete, func

from service.api.fact.filter import FactFilter
from service.api.fact.model import FactUpdate, FactCreate
from service.api.popular.model import MonthRanking
from service.common.exceptions import ObjectNotFound
from service.database.repositories.base_repository import AsyncBaseRepository
from service.models import Fact


class FactRepository(AsyncBaseRepository):
    async def create(self, fact_model: FactCreate) -> Fact:
        fact = Fact(**fact_model.model_dump())
        self.async_session.add(fact)
        await self.async_session.flush()
        return fact

    async def get_by_date(self, day: int, month: str) -> Optional[Fact]:
        query = select(Fact).where(Fact.day == day, Fact.month == month)
        result = await self.async_session.execute(query)
        return result.scalar_one_or_none()

    async def list(self, filter_: Optional[FactFilter]) -> Optional[List[Fact]]:
        query = select(Fact)
        if filter_ and filter_.day is not None:
            query = query.where(Fact.day == filter_.day)
        if filter_ and filter_.month is not None:
            query = query.where(Fact.month == filter_.month)

        result = await self.async_session.execute(query)
        return result.scalars().unique().all()

    async def update(self, fact_model: FactUpdate, fact: Fact) -> Fact:
        fact.update_data(**fact_model.model_dump())
        self.async_session.add(fact)
        await self.async_session.flush()
        return fact

    async def delete(self, fact_id: int) -> None:
        query = delete(Fact).where(Fact.id == fact_id)
        result = await self.async_session.execute(query)
        if not result:
            raise ObjectNotFound("Fact")
        await self.async_session.flush()

    async def get_popular_months(self) -> List[MonthRanking]:
        # Group facts by month, count the number of facts for each month,
        # and order the results in descending order of the count
        stmt = (
            select(Fact.id, Fact.month, func.count(Fact.id).label("days_checked"))
            .group_by(Fact.month)
            .order_by(func.count(Fact.id).desc())
        )
        result = await self.async_session.execute(stmt)
        popular_facts = result.fetchall()
        return [
            MonthRanking(id=row[0], month=row[1], days_checked=row[2])
            for row in popular_facts
        ]
