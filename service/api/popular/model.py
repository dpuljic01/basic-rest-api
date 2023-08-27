from pydantic import BaseModel


class MonthRanking(BaseModel):
    id: int
    month: str
    days_checked: int
