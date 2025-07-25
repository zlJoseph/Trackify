from contexts.auth.domain.repositories.user_repository import UserRepository
from contexts.auth.infrastructure.jwt.jwt_service import JWTService
from contexts.auth.application.dtos.login_dto import LoginDTO
from contexts.auth.domain.exceptions.invalid_password_exception import InvalidPasswordException

class LoginUseCase:
    def __init__(self, user_repository: UserRepository, jwt_service: JWTService):
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    async def execute(self, login_dto: LoginDTO) -> str:
        user = await self.user_repository.get_by_email(login_dto.email)

        if not user or not user.password.verify(login_dto.password):
            raise InvalidPasswordException("Credenciales inválidas")

        
        return self.jwt_service.generate_token({
            "id": user.id,
            "email": user.email
        })