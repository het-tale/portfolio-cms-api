from typing import Annotated, Optional
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from fastapi.responses import JSONResponse
from pydantic import HttpUrl

from app.dependencies import SessionDep, get_current_user
from app.schemas.project import ProjectBase
import cloudinary
import cloudinary.uploader

from app.services.project import project_service


from app.utils.enums import ProjectStatus

project_router = APIRouter(
    tags=["Projects"],
    prefix="/projects",
    dependencies=[Depends(get_current_user)]
)


@project_router.get("/get_all_projects")
async def get_projects_list(
    session: SessionDep,
    search: Annotated[str, Query()] = None,
    skip: int = 0,
    limit: int = 10,
):
    projects_list = await project_service.get_all_projects(
        session,
        search,
        skip,
        limit
    )
    return projects_list


@project_router.get("/get_project_by_id/{project_id}")
async def get_project_by_id(session: SessionDep, project_id: str):
    project = await project_service.get_project_by_id(session, project_id)
    return JSONResponse(
        content={
            "project_id": str(project.project_id),
            "title": project.title,
            "description": project.description,
            "status": project.status.value,
            "github_link": project.github_link,
            "website_link": project.website_link,
            "illustration": project.illustration,
        }
    )


@project_router.post("/create_project")
async def create_project(
    session: SessionDep,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    project_status: Annotated[ProjectStatus, Form()],
    github_link: Annotated[Optional[HttpUrl], Form()],
    website_link: Annotated[Optional[HttpUrl], Form()],
    project_img: Annotated[UploadFile, File()],
):
    if await project_service.is_project_exist(
        session, title, description, github_link, website_link
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project already Exist"
        )
    upload_result = cloudinary.uploader.upload(project_img.file)
    image_url = upload_result["secure_url"]
    project_in = ProjectBase(
        title=title,
        description=description,
        status=project_status,
        github_link=github_link,
        website_link=website_link,
        illustration=image_url,
    )
    project = await project_service.create_project(session, project_in)
    return JSONResponse(
        content={
            "title": project.title,
            "description": project.description,
            "status": project.status.value,
            "github_link": project.github_link,
            "website_link": project.website_link,
            "illustration": project.illustration,
        }
    )


@project_router.put("/update_project/{project_id}")
async def edit_project(
    session: SessionDep,
    project_id: str,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    project_status: Annotated[ProjectStatus, Form()],
    github_link: Annotated[Optional[HttpUrl], Form()],
    website_link: Annotated[Optional[HttpUrl], Form()],
    project_img: Annotated[UploadFile, File()],
):
    project = await project_service.get_project_by_id(session, project_id)
    upload_result = cloudinary.uploader.upload(project_img.file)
    image_url = upload_result["secure_url"]
    project_in = ProjectBase(
        title=title,
        description=description,
        status=project_status,
        github_link=github_link,
        website_link=website_link,
        illustration=image_url,
    )
    project = await project_service.update_project(
        session,
        project_in,
        project)
    return JSONResponse(
        content={
            "project_id": project.project_id,
            "title": project.title,
            "description": project.description,
            "status": project.status.value,
            "github_link": project.github_link,
            "website_link": project.website_link,
            "illustration": project.illustration,
        }
    )


@project_router.delete("/delete_project/{project_id}")
async def delete_project(session: SessionDep, project_id: str):
    try:
        project_to_delete = await project_service.get_project_by_id(
            session,
            project_id
            )
        await project_service.delete_project_by_id(session, project_to_delete)
        return {
            "message": "Project deleted successfully",
            "project_id": str(project_to_delete.project_id),
        }
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project Not Found"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request"
        )
