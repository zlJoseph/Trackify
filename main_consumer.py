import asyncio
from interfaces.consumers.rabbitmq.user_created_consumer import run_user_created_consumer
from interfaces.consumers.rabbitmq.auth_user_created_consumer import run_auth_user_created_consumer

async def main():
    await asyncio.gather(
        run_user_created_consumer(),
        run_auth_user_created_consumer(),
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(" [!] Exiting consumers")