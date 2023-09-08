from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field, field_validator, FieldValidationInfo


class FactBase(BaseModel):
    month: int = Field(..., ge=1, le=12, description="Month must be between 1 and 12")
    day: int = Field(..., ge=1, le=31, description="Day must be between 1 and 31")


class FactRequest(FactBase):
    @field_validator("day")
    def validate_day(cls, day: int, values: FieldValidationInfo) -> int:
        assert values.data
        try:
            date(year=date.today().year, month=values.data.get("month"), day=day)
        except ValueError:
            raise ValueError("Invalid date")
        return day


class FactCreate(FactBase):
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
