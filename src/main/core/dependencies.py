from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from ..database.session import async_session_local
from ..config import Settings, get_settings

settings: Settings = get_settings()


# dependency for get asynchronous database session
@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_local() as db:
        try:
            yield db
        finally:
            await db.close()
