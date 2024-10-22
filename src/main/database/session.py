from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from ..config import Settings, get_settings

settings: Settings = get_settings()


# create Asynchronous engine and session
async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)  # type: ignore
async_session_local = async_sessionmaker(async_engine, expire_on_commit=False)


