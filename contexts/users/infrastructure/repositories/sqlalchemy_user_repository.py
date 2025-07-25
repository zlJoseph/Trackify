from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from contexts.users.domain.entities.user import User
from contexts.users.domain.repositories.user_repository import UserRepository
from contexts.users.domain.value_objects.full_name import FullName
from contexts.users.domain.value_objects.email import Email
from contexts.users.domain.value_objects.password import Password
from contexts.users.domain.value_objects.gender import Gender
from contexts.users.domain.value_objects.age import Age
from contexts.users.domain.value_objects.user_id import UserId
from contexts.users.infrastructure.models.user_model import UserModel
from contexts.users.infrastructure.models_read.user_read_model import UserReadModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> None:
        orm_user = UserModel(
            id=user.id.value,
            first_name=user.full_name.first_name,
            last_name=user.full_name.last_name,
            middle_name=user.full_name.middle_name,
            email=user.email.value,
            password=user.password.value,
            gender=user.gender.value,
            age=user.age.value
        )
        self.session.add(orm_user)
        await self.session.commit()

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self.session.execute(
            select(UserReadModel).where(UserReadModel.id == user_id)
        )
        user_row = result.scalars().first()

        if not user_row:
            return None

        return User(
            id=UserId(user_row.id),# type: ignore
            full_name=FullName(
                user_row.first_name,# type: ignore
                user_row.last_name,# type: ignore
                user_row.middle_name# type: ignore
            ),
            email=Email(user_row.email),# type: ignore
            password=Password(""),# type: ignore
            gender=Gender(user_row.gender),# type: ignore
            age=Age(user_row.age)# type: ignore
        )
