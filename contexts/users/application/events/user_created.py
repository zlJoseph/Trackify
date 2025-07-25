from dataclasses import dataclass
from uuid import UUID
from shared.domain.events.event import DomainEvent
from contexts.users.domain.value_objects.full_name import FullName

@dataclass
class UserCreatedEvent(DomainEvent):
    email: str
    password: str
    first_name: str
    last_name: str
    middle_name: str
    gender: str
    age: int

    def __init__(self, user_id: UUID, email: str, password: str, full_name: FullName, gender: str, age: int):
        super().__init__(aggregate_id=user_id, event_name="user.created")
        self.first_name = full_name.first_name
        self.last_name = full_name.last_name
        self.middle_name = full_name.middle_name
        self.email = email
        self.password = password
        self.gender = gender
        self.age = age

    def to_dict(self) -> dict:
        return {
            "aggregate_id": str(self.aggregate_id),
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "gender": self.gender,
            "age": self.age
        }
