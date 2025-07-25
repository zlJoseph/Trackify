from dataclasses import dataclass
from abc import ABC, abstractmethod
from uuid import UUID

@dataclass
class DomainEvent(ABC):
    aggregate_id: UUID
    event_name: str

    @abstractmethod
    def to_dict(self) -> dict:
        pass
