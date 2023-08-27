from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field


class FactRequest(BaseModel):
    month: int = Field(..., ge=1, le=12, description="Month must be between 1 and 12")
    day: int = Field(..., ge=1, le=31, description="Day must be between 1 and 31")


class FactCreate(FactRequest):
    day: int
    month: str
    fact: str


class FactUpdate(BaseModel):
    fact: str


class FactResponse(BaseModel):
    id: int
    day: int
    month: str
    fact: str
