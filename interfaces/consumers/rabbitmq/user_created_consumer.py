import json
import asyncio
from pamqp.common import Arguments
from aio_pika.abc import AbstractIncomingMessage
from aio_pika.exceptions import AMQPException
from aio_pika import Message, connect_robust, ExchangeType
from shared.config.settings import settings
from interfaces.consumers.rabbitmq.handlers.user_created_handler import handle_user_created_event

QUEUE_NAME = "users.user_created.queue"
EXCHANGE_NAME = "trackify.fanout"
MAX_RETRIES = 3
RETRY_HEADER = "x-retry-count"

async def on_message(message: AbstractIncomingMessage):
    try:
        async with message.process(ignore_processed=True):
            payload = json.loads(message.body)
            print(payload)
            await handle_user_created_event(payload)
    except (json.JSONDecodeError, AMQPException) as exc:
        await handle_retry_logic(message, exc)

    except Exception as exc: # pylint: disable=broad-exception-caught
        print("Unhandled error in user_created consumer")
        await handle_retry_logic(message, exc)


async def handle_retry_logic(message: AbstractIncomingMessage, exc: Exception):
    headers = message.headers or {}
    retry_count = parse_retry_count(headers)

    print(f"Processing failed: {exc}")
    print(f"Retry count: {retry_count}")

    if retry_count < MAX_RETRIES:
        await message.reject(requeue=False)

        channel = message.channel
        retry_exchange = await channel.get_exchange("users.user_created.direct")# type: ignore

        new_headers = dict(headers)
        new_headers[RETRY_HEADER] = retry_count + 1

        retry_msg = Message(
            body=message.body,
            headers=new_headers,
            content_type=message.content_type,
            delivery_mode=2
        )

        await retry_exchange.publish(retry_msg, routing_key="retry")

    else:
        print("[X] Max retries reached. Sending to DLQ.")
        await message.reject(requeue=False)

def parse_retry_count(headers: dict, header_key: str = "x-retry-count") -> int:
    raw_value = headers.get(header_key, 0)

    try:
        if isinstance(raw_value, (int, float, str)):
            return int(raw_value)
    except (ValueError, TypeError):
        pass

    # Valor no válido
    return 0

async def run_user_created_consumer():
    connection = await connect_robust(settings.rabbitmq_url)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    exchange = await channel.declare_exchange(EXCHANGE_NAME, ExchangeType.FANOUT, durable=True)

    arguments: Arguments = {
        'x-dead-letter-exchange': 'users.user_created.dlx'
    }
    queue = await channel.declare_queue(QUEUE_NAME, durable=True, arguments=arguments)
    await queue.bind(exchange)

    await queue.consume(on_message)
    print(f"[✓] Listening for messages on queue '{QUEUE_NAME}'")

    await asyncio.Future()
