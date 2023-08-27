from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Header, Query
from httpx import HTTPStatusError

from service.api.fact.filter import FactFilter
from service.api.fact.model import FactResponse, FactUpdate, FactCreate, FactRequest
from service.common.utils import (
    get_repository_manager,
    get_numbers_api_client,
    check_api_key,
    get_month_name,
)
from service.database.repositories.manager import RepositoryManager

fact_router = APIRouter(prefix="/dates", tags=["DATES"])


def get_facts_filter(
    month: Optional[int] = Query(
        default=None, description="Used to search facts by month."
    ),
    day: Optional[int] = Query(
        default=None, description="Used to search facts by day."
    ),
) -> FactFilter:
    return FactFilter(month=month, day=day)


@fact_router.post("/", response_model=FactResponse)
async def upsert_fact(
    request: FactRequest,
    repository: RepositoryManager = Depends(get_repository_manager),
) -> FactResponse:
    try:
        numbers_api_client = get_numbers_api_client()
        fact_response = await numbers_api_client.get_fact(request)
    except HTTPStatusError as err:
        raise HTTPException(
            status_code=err.response.status_code, detail=err.response.json()
        )

    month_name = get_month_name(request.month)
    existing_fact = await repository.fact_repository.get_by_date(
        request.day, month_name
    )
    fact_create = FactCreate(day=request.day, month=month_name, fact=fact_response)
    if not existing_fact:
        fact_db = await repository.fact_repository.create(fact_create)
    else:
        update_model = FactUpdate(fact=fact_response)
        fact_db = await repository.fact_repository.update(
            fact_model=update_model, fact=existing_fact
        )
    return fact_db.to_model()


@fact_router.get("/", response_model=List[FactResponse])
async def list_facts(
    filter_: FactFilter = Depends(get_facts_filter),
    repository: RepositoryManager = Depends(get_repository_manager),
) -> List[FactResponse]:
    all_facts = await repository.fact_repository.list(filter_)
    return [fact.to_model() for fact in all_facts]


@fact_router.delete("/{fact_id}")
async def delete_fact_by_id(
    fact_id: int,
    x_api_key: str = Header(..., description="API Key"),
    repository: RepositoryManager = Depends(get_repository_manager),
) -> dict:
    check_api_key(x_api_key)
    await repository.fact_repository.delete(fact_id)
    return {"status": "Deleted!"}
