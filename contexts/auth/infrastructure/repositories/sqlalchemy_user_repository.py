from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from contexts.auth.domain.entities.user import User
from contexts.auth.domain.repositories.user_repository import UserRepository
from contexts.auth.domain.value_objects.password import Password
from contexts.auth.infrastructure.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user_row = result.scalars().first()

        if not user_row:
            return None

        return User(
            id=str(user_row.id),# type: ignore
            email=user_row.email,# type: ignore
            password=Password(user_row.password),# type: ignore
        )
