from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
import uuid
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict, expiry_time: timedelta | None, refresh: bool = False
):
    expire = (
        datetime.now(timezone.utc) + expiry_time
        if expiry_time is not None
        else timedelta(
            seconds=(
                settings.ACCESS_TOKEN_EXPIRE_MINUTES
                if not refresh
                else settings.REFRESH_TOKEN_EXPIRE_DAYS
            )
        )
    )
    payload = {
        "exp": expire,
        "user": data,
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }
    token = jwt.encode(
        payload=payload,
        key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return token
