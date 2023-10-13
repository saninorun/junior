import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from settings import settings

engine = create_async_engine(
    settings.database_url,
    echo=False,
)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_session() -> async_session:
    """
    Функция для создания сессии с БД и возвращения ее вызвавшей. После завершения \
    действий вызывающей стороны, дополнительно гарантирует закрытие сессии.

    """
    try:
        async with async_session() as session:
            yield session
    finally:
        await session.close()
        await engine.dispose()