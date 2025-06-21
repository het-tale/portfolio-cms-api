from typing import Optional
from sqlmodel import Column, Field, SQLModel
from datetime import datetime, timezone
import sqlalchemy.dialects.postgresql as pg
import uuid

from ..utils.enums import Category


class Skill(SQLModel, table=True):
    __tablename__ = "skills"

    skill_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), nullable=False,
                         primary_key=True),
        default_factory=uuid.uuid4,
    )
    name: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False,
                                       unique=True))

    category: Category = Field(
        sa_column=Column(pg.ENUM(Category, name="category_enum"),
                         nullable=False)
    )
    years_of_experience: Optional[int] = Field(sa_column=Column(pg.INTEGER))

    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )
    # Many to many relationship with projects
    # projects: list["Project"] = Relationship(
    #     back_populates="skills", link_model=ProjectSkill
    # )
