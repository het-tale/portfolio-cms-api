from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.dependencies import CurrentUserDep


admin_router = APIRouter(tags=["Admin"])


@admin_router.get("/user/me")
async def get_user(current_user: CurrentUserDep):
    return JSONResponse(
        content={
            "user_id": str(current_user.id),
            "email": current_user.email,
            "username": current_user.username,
        }
    )
