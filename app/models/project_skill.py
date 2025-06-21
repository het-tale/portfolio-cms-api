from sqlmodel import Column, Field, SQLModel, ForeignKey
import sqlalchemy.dialects.postgresql as pg
import uuid


class ProjectSkill(SQLModel, table=True):
    __tablename__ = "project_skill"

    project_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            ForeignKey("projects.project_id", ondelete="CASCADE"),
            nullable=False,
            primary_key=True,
        )
    )
    skill_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            ForeignKey("skills.skill_id", ondelete="CASCADE"),
            nullable=False,
            primary_key=True,
        )
    )
