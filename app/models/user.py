from sqlmodel import Field, SQLModel, Column
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
import uuid


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4
        )
    )
    username: str
    email: str
    password: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,
                                                  default=datetime.now()))
