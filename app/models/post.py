from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel, Column
import uuid
import sqlalchemy.dialects.postgresql as pg


class Post(SQLModel, table=True):
    __tablename__ = "posts"

    post_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True),
        default_factory=uuid.uuid4,
    )
    title: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False,
                                        unique=True))
    summary: Optional[str] = Field(sa_column=Column(pg.VARCHAR(255),
                                                    unique=True))
    content: str = Field(sa_column=Column(pg.TEXT))
    slug: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False,
                                       unique=True))
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )
