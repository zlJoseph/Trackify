from pydantic import BaseModel
from uuid import UUID

class UserResponseDTO(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    middle_name: str
    email: str
    gender: str
    age: int
