from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate


engine = create_async_engine(url=settings.DATABASE_URL, echo=True)


async def init_db():
    if settings.ENV == "development":
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)


async def init_database(session: AsyncSession):
    from app.services.user import user_service

    user = (
        await session.exec(select(User).where(settings.ADMIN == User.email))
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.ADMIN,
            password=settings.ADMIN_PASSWORD,
            username=settings.ADMIN_USERNAME,
        )
        user = await user_service.create_user(session=session,
                                              user_create=user_in)
