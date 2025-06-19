from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import settings
from app.dependencies import SessionDep
from app.models.user import User
from ..services.user import user_service
from ..core.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

auth_router = APIRouter(tags=["Login"])


@auth_router.post("/login")
async def login(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
) -> JSONResponse:
    email = user_data.username
    password = user_data.password
    db_user: User = await user_service.authenticate(
        session=session, email=email, password=password
    )
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
    refresh_token_expire = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_access_token(
        data={"email": db_user.email, "id": str(db_user.id)},
        refresh=True,
        expiry_time=refresh_token_expire,
    )
    res = JSONResponse(
        content={
            "message": "Login succeful",
            "access_token": access_token,
            "user": {"email": db_user.email, "uid": str(db_user.id)},
        }
    )
    res.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return res
