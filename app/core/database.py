from sqlmodel import SQLModel
from .config import settings
from sqlalchemy.ext.asyncio import create_async_engine


engine = create_async_engine(url=settings.DATABASE_URL, echo=True)


async def init_db():
    if settings.ENV == "development":
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
