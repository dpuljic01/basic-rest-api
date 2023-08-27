from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from service.api.fact.model import FactResponse
from service.database.db import Base


class Fact(Base):
    __tablename__ = "facts"

    id: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[int] = mapped_column(nullable=False)
    day: Mapped[int] = mapped_column(nullable=False)
    fact: Mapped[str] = mapped_column(nullable=False)

    __table_args__ = (UniqueConstraint("day", "month", name="uq_fact_day_month"),)

    def to_model(self) -> FactResponse:
        return FactResponse(id=self.id, day=self.day, month=self.month, fact=self.fact)
