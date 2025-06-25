from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.database import engine
from fastapi.security import OAuth2PasswordBearer

from app.models.user import User
from app.schemas.user import TokenPayload


async def get_session():
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False)
    async with Session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str:
        token = request.cookies.get("access_token")
        if not token:
            # fallback to Authorization header
            auth = request.headers.get("Authorization")
            if auth and auth.startswith("Bearer "):
                token = auth[7:]
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return token


reusable_oath2 = OAuth2PasswordBearerWithCookie(tokenUrl="login")
TokenDep = Annotated[str, Depends(reusable_oath2)]


async def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, key=settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM
        )
        token_data = TokenPayload(**payload)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized")
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await session.get(User, token_data.user["id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
