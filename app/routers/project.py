from fastapi import APIRouter

from app.dependencies import CurrentUserDep, SessionDep


project_router = APIRouter(tags=["Projects"], prefix="/projects")


@project_router.get('/')
def get_project(session: SessionDep, current_user: CurrentUserDep):
    return current_user
