import httpx

from service.api.fact.model import FactRequest


class NumbersAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_fact(self, fact_input: FactRequest) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/{fact_input.month}/{fact_input.day}/date"
            )
            response.raise_for_status()
        return response.text.strip()
