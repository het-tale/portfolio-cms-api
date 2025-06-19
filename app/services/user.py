from sqlmodel import select
from app.dependencies import SessionDep
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_hash_password, verify_password


class UserService:
    async def create_user(self, session: SessionDep, user_create: UserCreate):
        result = get_hash_password(user_create.password)
        user_obj = User.model_validate(user_create,
                                       update={"hashed_password": result})
        session.add(user_obj)
        await session.commit()
        await session.refresh(user_obj)
        return user_obj

    async def get_user_by_email(self, session: SessionDep,
                                email: str) -> User | None:
        statement = select(User).where(email == User.email)
        user = (await session.exec(statement)).first()
        return user

    async def authenticate(
        self, session: SessionDep, email: str, password: str
    ) -> User | None:
        user_db = await self.get_user_by_email(session=session, email=email)
        if not user_db:
            return None
        if not verify_password(password, user_db.hashed_password):
            return None
        return user_db


user_service = UserService()
