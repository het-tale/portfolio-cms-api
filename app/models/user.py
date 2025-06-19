from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Column
from datetime import datetime, timezone
import sqlalchemy.dialects.postgresql as pg
import uuid


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True),
        default_factory=uuid.uuid4,
    )
    username: str = Field(sa_column=Column(pg.VARCHAR(50), nullable=False,
                                           unique=True))
    email: EmailStr = Field(
        sa_column=Column(pg.VARCHAR(255), nullable=False, unique=True)
    )
    hashed_password: str = Field(
        sa_column=Column(pg.VARCHAR(128), nullable=False), exclude=True
    )
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )
