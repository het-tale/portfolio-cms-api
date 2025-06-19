from fastapi import APIRouter
from .auth import auth_router
from .project import project_router


api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(project_router)
