from uuid import UUID
from contexts.users.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from contexts.users.application.query.user_response_dto import UserResponseDTO

class GetUserByIdUseCase:
    def __init__(self, repository: SQLAlchemyUserRepository):
        self.repository = repository

    async def execute(self, user_id: UUID) -> UserResponseDTO | None:
        user = await self.repository.get_by_id(user_id)

        if not user:
            return None
        
        return UserResponseDTO(
            id=user.id.value,
            first_name=user.full_name.first_name,
            last_name=user.full_name.last_name,
            middle_name=user.full_name.middle_name,
            email=user.email.value,
            gender=user.gender.value,
            age=user.age.value
        )
