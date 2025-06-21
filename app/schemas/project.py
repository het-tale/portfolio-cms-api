from typing import Optional
from pydantic import BaseModel, HttpUrl
from ..utils.enums import ProjectStatus


class ProjectBase(BaseModel):
    title: str
    description: str
    status: ProjectStatus
    github_link: Optional[HttpUrl]
    website_link: Optional[HttpUrl]
    illustration: str


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    github_link: Optional[HttpUrl] = None
    website_link: Optional[HttpUrl] = None
    illustration: Optional[str] = None
