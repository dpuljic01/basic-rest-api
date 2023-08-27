from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


@dataclass
class AsyncBaseRepository:
    async_session: AsyncSession
    async_engine: AsyncEngine
