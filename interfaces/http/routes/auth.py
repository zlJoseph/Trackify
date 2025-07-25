from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from shared.infrastructure.db.session import get_session
from contexts.auth.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from contexts.auth.application.dtos.login_dto import LoginDTO
from contexts.auth.application.use_case.login_use_case import LoginUseCase
from contexts.auth.infrastructure.jwt.jwt_service import JWTService
from interfaces.http.schemas.login_request import LoginRequest

router = APIRouter()

@router.post("/", status_code=status.HTTP_200_OK)
async def login(
    request: LoginRequest,
    session: AsyncSession = Depends(get_session)
):
    print("[DEBUG] Payload recibido:", request)
    user_repo = SQLAlchemyUserRepository(session)
    jwt_service = JWTService()
    use_case = LoginUseCase(user_repo, jwt_service)

    dto = LoginDTO(
        email=request.email,
        password=request.password
    )

    token = await use_case.execute(dto)
    return {"token": token}
