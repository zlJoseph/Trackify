from abc import ABC, abstractmethod
from typing import Optional
from contexts.auth.domain.entities.user import User

class UserRepository(ABC):

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass