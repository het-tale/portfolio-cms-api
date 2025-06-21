from typing import Optional
from pydantic import BaseModel

from app.utils.enums import Category


class SkillBase(BaseModel):
    name: str
    category: Category
    years_of_experience: int | None


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[Category] = None
    years_of_experience: Optional[int] = None
