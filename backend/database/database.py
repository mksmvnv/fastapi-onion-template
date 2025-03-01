from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings


async_engine = create_async_engine(url=settings.database.url)

async_session_maker = async_sessionmaker(
    bind=async_engine, autoflush=False, expire_on_commit=False
)
