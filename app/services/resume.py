from typing import Annotated
from fastapi import File, HTTPException, UploadFile, status
import cloudinary
import cloudinary.uploader
from sqlmodel import delete, select, update
from app.dependencies import SessionDep
from app.models.resume import Resume
from app.schemas.resume import ResumeBase


class ResumeService:
    async def upload_resume(
        self, session: SessionDep, resume_file: Annotated[UploadFile, File()]
    ):
        await session.exec(delete(Resume))
        await session.commit()
        upload_result = cloudinary.uploader.upload(resume_file.file)
        new_resume_url = upload_result["secure_url"]
        new_resume = ResumeBase(resume_link=new_resume_url, views_counter=0)
        db_resume = Resume(
            resume_link=str(new_resume.resume_link),
            views_counter=new_resume.views_counter,
        )
        session.add(db_resume)
        await session.commit()
        await session.refresh(db_resume)
        return db_resume

    async def get_resume(self, session: SessionDep):
        statement = select(Resume)
        resume_db = (await session.exec(statement)).first()
        if not resume_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume Not Exist. Please Upload a new one",
            )
        await session.exec(
            update(Resume).values(views_counter=Resume.views_counter + 1)
        )
        await session.commit()
        await session.refresh(resume_db)
        return resume_db

    async def delete_resume(self, session: SessionDep):
        await session.exec(delete(Resume))
        await session.commit()


resume_service = ResumeService()
