from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.database import engine, init_database
import asyncio


async def init() -> None:
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with Session() as session:
        await init_database(session)


def main() -> None:
    print("Creating initial data")
    asyncio.run(init())
    print("Initial data created")


if __name__ == "__main__":
    main()
