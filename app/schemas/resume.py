from typing import Optional
from pydantic import BaseModel, Field, HttpUrl


class ResumeBase(BaseModel):
    resume_link: Optional[HttpUrl]
    views_counter: int = Field(default=0)


# class ResumeUpdate(ResumeBase):
#     views_counter: int = Field(default=0)
