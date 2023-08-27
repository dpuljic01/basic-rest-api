from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase

from service.settings import settings

async_engine: AsyncEngine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL)
async_session: async_sessionmaker = async_sessionmaker(bind=async_engine)


class Base(DeclarativeBase):
    def update_data(self, **kwargs: dict[str, Any]) -> None:
        for key in kwargs:
            if hasattr(self, key) and key != "id":
                setattr(self, key, kwargs[key])


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
