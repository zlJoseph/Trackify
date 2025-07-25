from pydantic import BaseModel, EmailStr
from typing import Literal

class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    email: EmailStr
    password: str
    gender: Literal["M", "F", "NB"]
    age: int
