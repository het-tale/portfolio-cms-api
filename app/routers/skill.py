from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse

from app.dependencies import SessionDep, get_current_user
from app.schemas.skill import SkillBase, SkillUpdate
from ..services.skill import skill_service


skill_router = APIRouter(
    tags=["Skills"],
    prefix="/skill",
    dependencies=[Depends(get_current_user)])


@skill_router.get("/get_skills_list")
async def get_skills_list(
    session: SessionDep,
    search: Annotated[str, Query()] = None,
    skip: int = 0,
    limit: int = 10,
):
    return await skill_service.get_all_skills(
        session,
        search,
        skip,
        limit)


@skill_router.get("/get_skill_by_id/{skill_id}")
async def get_skill_by_id(session: SessionDep, skill_id: str):
    try:
        skill = await skill_service.get_skill_by_id(session, skill_id)
        return JSONResponse(
            content={
                "skill_id": str(skill.skill_id),
                "name": skill.name,
                "category": skill.category.value,
                "years_of_experience": skill.years_of_experience,
            }
        )
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Skill Not Found"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request"
        )


@skill_router.post("/create_skill")
async def create_skill(session: SessionDep, new_skill: SkillBase):
    skill = await skill_service.create_new_skill(session, new_skill)
    return JSONResponse(
        content={
            "skill_id": str(skill.skill_id),
            "name": skill.name,
            "category": skill.category.value,
            "years_of_experience": skill.years_of_experience,
        }
    )


@skill_router.put("/update_skill/{skill_id}")
async def update_skill(
    session: SessionDep,
    skill_id: str,
    update_skill: SkillUpdate
):
    updated_skill = await skill_service.edit_skill(
        session,
        skill_id,
        update_skill
    )
    return JSONResponse(
        content={
            "skill_id": str(updated_skill.skill_id),
            "name": updated_skill.name,
            "category": updated_skill.category.value,
            "years_of_experience": updated_skill.years_of_experience,
        }
    )


@skill_router.delete("/delete_skill/{skill_id}")
async def delete_skill(session: SessionDep, skill_id: str):
    try:
        await skill_service.delete_skill(session, skill_id)
        return {
            "message": "Skill deleted successfully",
            "skill_id": str(skill_id),
        }
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Skill Not Found"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request"
        )
