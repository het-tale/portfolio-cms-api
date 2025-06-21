from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlmodel import col, or_, select
from app.dependencies import SessionDep
from app.models.skill import Skill
from app.schemas.skill import SkillBase, SkillUpdate
from app.utils.enums import Category


class SkillService:
    async def get_all_skills(
            self,
            session: SessionDep,
            name: Optional[str] = None,
            category: Optional[Category] = None,
            skip: int = 0,
            limit: int = 10
            ):
        statement = select(Skill)
        filters = []
        if name:
            filters.append(col(Skill.name).ilike(f"%{name}%"))
        if category:
            filters.append(col(Skill.category) == category)
        if filters:
            statement = statement.where(or_(*filters))
        skills_list = (
            await session.exec(statement.offset(skip).limit(limit))
            ).all()
        return skills_list

    async def get_skill_by_id(self, session: SessionDep, skill_id: str):
        statement = select(Skill).where(Skill.skill_id == skill_id)
        skill = (await session.exec(statement)).first()
        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Skill Not Found"
            )
        return skill

    async def is_skill_exist(self, session: SessionDep, name: str):
        statement = select(Skill).where(
            func.lower(func.trim(Skill.name)) == name.strip().lower()
        )
        skill = (await session.exec(statement)).first()
        print("Helloooo skill", skill)
        if skill:
            return True
        return False

    async def create_new_skill(
            self,
            session: SessionDep,
            new_skill: SkillBase):
        if await self.is_skill_exist(session, new_skill.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skill Already Exist"
            )
        created_skill = Skill.model_validate(new_skill)
        session.add(created_skill)
        await session.commit()
        await session.refresh(created_skill)
        return created_skill

    async def edit_skill(
            self,
            session: SessionDep,
            skill_id: str,
            update_skill: SkillUpdate
    ):
        skill_to_update = await self.get_skill_by_id(session, skill_id)
        new_skill = update_skill.model_dump(exclude_unset=True)
        for key, value in new_skill.items():
            setattr(skill_to_update, key, value)
        skill_to_update.updated_at = datetime.now(timezone.utc)
        session.add(skill_to_update)
        await session.commit()
        await session.refresh(skill_to_update)
        return skill_to_update

    async def delete_skill(self, session: SessionDep, skill_id: str):
        skill_to_delete = await self.get_skill_by_id(session, skill_id)
        await session.delete(skill_to_delete)
        await session.commit()


skill_service = SkillService()
