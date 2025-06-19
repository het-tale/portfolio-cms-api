from app.dependencies import SessionDep
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_hash_password


class UserService:
    async def create_user(self, session: SessionDep, user_create: UserCreate):
        result = await get_hash_password(user_create.password)
        user_obj = User.model_validate(
            user_create,
            update={"hashed_password": result}
        )
        session.add(user_obj)
        await session.commit()
        await session.refresh(user_obj)
        return user_obj


user_service = UserService()
