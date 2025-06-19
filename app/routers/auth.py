from datetime import timedelta
from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.dependencies import SessionDep
from app.models.user import User
from ..services.user import user_service
from ..core.security import create_access_token
from ..schemas.user import Token, UserLogin
from fastapi.responses import JSONResponse

auth_router = APIRouter(tags=["Login"])


@auth_router.post("/login")
async def login(user_data: UserLogin, session: SessionDep) -> Token:
    email = user_data.email
    password = user_data.password
    db_user: User = await user_service.authenticate(
        session=session, email=email, password=password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Email or Password",
        )
    access_token_expire = timedelta(
        seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": db_user.email, "id": str(db_user.id)},
        expiry_time=access_token_expire,
    )
    refresh_token = create_access_token(
        data={"email": db_user.email, "id": str(db_user.id)},
        refresh=True,
        expiry_time=access_token_expire,
    )
    return JSONResponse(
        content={
            "message": "Login succeful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "email": db_user.email,
                "uid": str(db_user.id)
            }
        }
    )
