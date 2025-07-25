from fastapi import APIRouter, Depends, status, HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from shared.infrastructure.db.session import get_session
from shared.infrastructure.messaging.rabbitmq_event_bus import RabbitMQEventBus
from contexts.users.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from contexts.users.application.commands.create_user import CreateUserCommand
from contexts.users.application.handlers.create_user_handler import CreateUserHandler
from contexts.users.application.query.user_response_dto import UserResponseDTO
from contexts.users.application.query.get_user_by_id_use_case import GetUserByIdUseCase
from interfaces.http.schemas.create_user_request import CreateUserRequest
from interfaces.http.middlewares.auth_middleware import get_current_user_token

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    session: AsyncSession = Depends(get_session)
):
    user_repo = SQLAlchemyUserRepository(session)
    event_bus = RabbitMQEventBus()
    handler = CreateUserHandler(user_repo, event_bus)

    command = CreateUserCommand(
        first_name=request.first_name,
        last_name=request.last_name,
        middle_name=request.middle_name,
        email=request.email,
        password=request.password,
        gender=request.gender,
        age=request.age
    )

    await handler.handle(command)
    return {"message": "User created successfully"}

@router.get("/{user_id}", response_model=UserResponseDTO)
async def get_user_by_id(
    user_id: UUID,
    _: dict = Depends(get_current_user_token),
    session: AsyncSession = Depends(get_session)
):
    repo = SQLAlchemyUserRepository(session)
    use_case = GetUserByIdUseCase(repo)

    user = await use_case.execute(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
