from abc import ABC, abstractmethod
from shared.domain.events.event import DomainEvent

class EventBus(ABC):

    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        """Publica un evento en el bus de eventos (RabbitMQ, Kafka, etc.)"""
