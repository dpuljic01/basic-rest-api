from dataclasses import dataclass


@dataclass
class FactFilter:
    day: int | None = None
    month: int | None = None
