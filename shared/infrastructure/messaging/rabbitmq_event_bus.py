import json
from aio_pika import connect_robust, Message, ExchangeType
from shared.config.settings import settings
from shared.domain.events.event_bus import EventBus
from shared.domain.events.event import DomainEvent

class RabbitMQEventBus(EventBus):
    def __init__(self):
        self._connection = None
        self._channel = None
        self._exchange = None

    async def connect(self):
        if not self._connection:
            self._connection = await connect_robust(settings.rabbitmq_url)
            self._channel = await self._connection.channel()
            self._exchange = await self._channel.declare_exchange(
                name="trackify.fanout",
                type=ExchangeType.FANOUT,
                durable=True,
                auto_delete=False
            )

    async def publish(self, event: DomainEvent):
        await self.connect()

        message = Message(
            body=json.dumps({
                "event_name": event.event_name,
                "data": event.to_dict()
            }).encode(),
            content_type="application/json"
        )

        assert self._exchange is not None
        await self._exchange.publish(message, routing_key="")

    async def close(self):
        if self._connection:
            await self._connection.close()
            self._connection = None
