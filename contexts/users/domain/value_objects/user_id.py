from dataclasses import dataclass
import uuid

@dataclass(frozen=True)
class UserId:
    value: uuid.UUID

    @staticmethod
    def new() -> "UserId":
        return UserId(uuid.uuid4())

    def __str__(self):
        return str(self.value)
