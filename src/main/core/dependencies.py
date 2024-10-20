from ..config import Settings, get_settings
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from ..database.session import async_session_local

settings: Settings = get_settings()


# dependency for get asynchronous database session
@asynccontextmanager
async def get_session() -> AsyncGenerator:
    async with async_session_local() as db:
        try:
            yield db
        finally:
            await db.close()
