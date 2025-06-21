from typing import Annotated
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from app.dependencies import SessionDep, get_current_user
from app.services.resume import resume_service


resume_router = APIRouter(
    tags=["Resume"],
    prefix="/resume",
    dependencies=[Depends(get_current_user)]
    )


@resume_router.post("/upload_resume")
async def upload_resume(
    session: SessionDep, resume_file: Annotated[UploadFile, File()]
):
    resume = await resume_service.upload_resume(session, resume_file)
    return JSONResponse(
        content={
            "resume_link": resume.resume_link,
            "views_counter": resume.views_counter,
        }
    )


@resume_router.get("/get_resume")
async def get_resume(session: SessionDep):
    resume = await resume_service.get_resume(session)
    return JSONResponse(
        content={
            "resume_link": resume.resume_link,
            "views_counter": resume.views_counter,
        }
    )


@resume_router.delete("/delete_resume")
async def delete_resume(session: SessionDep):
    await resume_service.delete_resume(session)
