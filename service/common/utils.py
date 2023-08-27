from typing import AsyncGenerator

from service.common.api_clients import NumbersAPIClient
from service.common.exceptions import Unauthorized
from service.database.db import async_session, async_engine
from service.database.repositories.manager import RepositoryManager
from service.settings import settings

number_to_month = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


def get_month_name(month: int):
    return number_to_month.get(month, "Invalid month")


async def get_repository_manager() -> AsyncGenerator[RepositoryManager, None]:
    async with async_session() as session, session.begin():
        repository_manager = RepositoryManager(
            async_session=session, async_engine=async_engine
        )
        yield repository_manager


def get_numbers_api_client() -> NumbersAPIClient:
    return NumbersAPIClient(base_url=settings.NUMBERS_API_BASE_URL)


def check_api_key(x_api_key: str) -> None:
    if x_api_key != settings.NUMBERS_API_KEY:
        raise Unauthorized("Invalid API_KEY")
