from datetime import timedelta
from typing import Annotated, Optional
from fastapi import APIRouter, Cookie, Depends, HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from pydantic import ValidationError
from app.core.config import settings
from app.dependencies import CurrentUserDep, SessionDep
from app.models.user import User
from app.schemas.user import TokenPayload
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
    refresh_token_expire = timedelta(
        seconds=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_access_token(
        data={"email": db_user.email, "id": str(db_user.id)},
        refresh=True,
        expiry_time=refresh_token_expire,
    )
    res = JSONResponse(
        content={
            "message": "Logged in successfully",
            "access_token": access_token,
            "user": {"email": db_user.email, "uid": str(db_user.id)},
        }
    )
    res.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=True,
        path="/",
    )
    res.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="Lax",
        secure=True,
        path="/",
    )
    return res


@auth_router.post("/refresh_token")
async def get_new_access_token(
    session: SessionDep,
    refresh_token: Annotated[Optional[str],
                             Cookie()] = None
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    try:
        payload = jwt.decode(
            refresh_token,
            key=settings.SECRET_KEY,
            algorithms=settings.JWT_ALGORITHM,
        )
        print("refresh token payload", payload)
        if not payload.get("refresh"):
            raise HTTPException(status_code=401, detail="Invalid token type")

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    token_data = TokenPayload(**payload)
    user_db = await session.get(User, token_data.user["id"])
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    access_token = create_access_token(
        data={"email": user_db.email, "id": str(user_db.id)},
        expiry_time=timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    res = JSONResponse(
        content={
            "message": "New access token generated",
            "access_token": access_token,
        }
    )
    res.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=True,
        path="/",
    )
    return res


@auth_router.post("/logout")
def logout(current: CurrentUserDep):
    response = JSONResponse(
        content={
            "message": "Logged out successfully",
        }
    )
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")
    return response
