from enum import Enum
from typing import TYPE_CHECKING, Optional
from pydantic import HttpUrl
from sqlmodel import Column, Field, Relationship, SQLModel
from datetime import datetime, timezone
import sqlalchemy.dialects.postgresql as pg
import uuid

from app.models.project_skill import ProjectSkill

if TYPE_CHECKING:
    from app.models.skill import Skill


class ProjectStatus(Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    project_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), nullable=False,
                         primary_key=True),
        default_factory=uuid.uuid4,
    )
    title: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False,
                                        unique=True))

    description: str = Field(
        sa_column=Column(pg.VARCHAR(100), nullable=False, unique=True)
    )

    illustration: Optional[HttpUrl] = Field(
        sa_column=Column(pg.VARCHAR(500)), default=None
    )
    status: ProjectStatus = Field(
        sa_column=Column(pg.ENUM(ProjectStatus, name="projectstatus"),
                         nullable=False)
    )

    github_link: Optional[HttpUrl] = Field(
        sa_column=Column(pg.VARCHAR(500)), default=None
    )
    website_link: Optional[HttpUrl] = Field(
        sa_column=Column(pg.VARCHAR(500)), default=None
    )
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )
    # Many to many relationship with skills
    skills: list["Skill"] = Relationship(
        back_populates="projects", link_model=ProjectSkill
    )
