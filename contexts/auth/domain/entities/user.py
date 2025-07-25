from dataclasses import dataclass
from contexts.auth.domain.value_objects.password import Password

@dataclass(frozen=True)
class User:
    id: str
    email: str
    password: Password
