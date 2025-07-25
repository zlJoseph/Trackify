from dataclasses import dataclass

@dataclass
class CreateUserCommand:
    first_name: str
    last_name: str
    middle_name: str
    email: str
    password: str
    gender: str
    age: int
