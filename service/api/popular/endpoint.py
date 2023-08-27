from typing import List

from fastapi import APIRouter, Depends

from service.api.popular.model import MonthRanking
from service.common.utils import (
    get_repository_manager,
)
from service.database.repositories.manager import RepositoryManager

popular_router = APIRouter(prefix="/popular", tags=["POPULAR"])


@popular_router.get("/", response_model=List[MonthRanking])
async def get_popular_months(
    repository: RepositoryManager = Depends(get_repository_manager),
) -> List[MonthRanking]:
    return await repository.fact_repository.get_popular_months()
