from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from contexts.users.domain.entities.user import User

class UserRepository(ABC):

    @abstractmethod
    async def save(self, user: User) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        pass