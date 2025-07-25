from sqlalchemy import insert
from shared.infrastructure.db.session import get_session
from contexts.users.infrastructure.models_read.user_read_model import UserReadModel

async def handle_user_created_event(data: dict):
    payload = data["data"]
    async for session in get_session():
        stmt = insert(UserReadModel).values(
            id=payload["aggregate_id"],
            first_name=payload["first_name"],
            last_name=payload["last_name"],
            middle_name=payload["middle_name"],
            email=payload["email"],
            gender=payload["gender"],
            age=payload["age"]
        )
        await session.execute(stmt)
        await session.commit()
