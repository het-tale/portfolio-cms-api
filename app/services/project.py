from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException, status
from pydantic import HttpUrl
from sqlalchemy import String
from sqlmodel import cast, or_, select
from app.dependencies import SessionDep
from app.models.project import Project
from app.schemas.project import ProjectBase


class ProjectService:
    async def get_all_projects(
        self,
        session: SessionDep,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ):
        statement = select(Project)
        filters = []
        if search:
            filters.append((Project.title).ilike(f"%{search}%"))
            filters.append((Project.description).ilike(f"%{search}%"))
            filters.append(cast(Project.status, String).ilike(f"%{search}%"))
        if filters:
            statement = statement.where(or_(*filters))
        projects_list = (
            await session.exec(statement.offset(skip).limit(limit))).all()
        return projects_list

    async def get_project_by_id(self, session: SessionDep, project_id: str):
        statement = select(Project).where(Project.project_id == project_id)
        project = (await session.exec(statement)).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project Not Found"
            )
        return project

    async def is_project_exist(
        self,
        session: SessionDep,
        title: str,
        description: str,
        github_link: Optional[HttpUrl],
        website_link: Optional[HttpUrl],
    ):
        statement = select(Project).where(
            or_(
                Project.title == title,
                Project.description == description,
                Project.github_link == str(github_link),
                Project.website_link == str(website_link),
            )
        )
        project = (await session.exec(statement)).first()
        if project:
            return True
        return False

    async def create_project(
            self,
            session: SessionDep,
            project_in: ProjectBase):
        project_obj = Project(
            title=project_in.title,
            description=project_in.description,
            status=project_in.status,
            github_link=str(project_in.github_link),
            website_link=str(project_in.website_link),
            illustration=project_in.illustration,
        )
        session.add(project_obj)
        await session.commit()
        await session.refresh(project_obj)
        return project_obj

    async def update_project(
        self,
        session: SessionDep,
        project_in: ProjectBase,
        project_to_update: Project
    ):
        update_project = project_in.model_dump(exclude_unset=True)
        for key, value in update_project.items():
            if key in {"github_link", "website_link"} and value is not None:
                value = str(value)
            setattr(project_to_update, key, value)
        project_to_update.updated_at = datetime.now(timezone.utc)
        session.add(project_to_update)
        await session.commit()
        await session.refresh(project_to_update)
        return project_to_update

    async def delete_project_by_id(
        self, session: SessionDep, project_to_delete: Project
    ):
        await session.delete(project_to_delete)
        await session.commit()


project_service = ProjectService()
