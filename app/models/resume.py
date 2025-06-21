from datetime import datetime, timezone
from typing import Optional
from pydantic import HttpUrl
from sqlmodel import Field, SQLModel, Column
import uuid
import sqlalchemy.dialects.postgresql as pg


class Resume(SQLModel, table=True):
    __tablename__ = "resume"

    resume_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True),
        default_factory=uuid.uuid4,
    )
    resume_link: Optional[HttpUrl] = Field(
        sa_column=Column(pg.VARCHAR(500)), default=None
    )
    views_counter: int = Field(default=0, nullable=False)
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )
