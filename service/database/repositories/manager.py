from dataclasses import dataclass

from service.database.repositories.base_repository import AsyncBaseRepository
from service.database.repositories.fact_repository import FactRepository


@dataclass
class RepositoryManager(AsyncBaseRepository):
    @property
    def fact_repository(self) -> FactRepository:
        return FactRepository(self.async_session, self.async_engine)
