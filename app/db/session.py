from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker

from core.settings import settings


class DatabaseHelper:

    def __init__(self, url: str):
        self._engine: AsyncEngine = create_async_engine(url)
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self):
        await self._engine.dispose()

    async def session_getter(self):
        async with self._session_factory() as session:
            yield session


db_helper = DatabaseHelper(str(settings.DATABASE_URL))


async def get_session():
    async for session in db_helper.session_getter():
        yield session
