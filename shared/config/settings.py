from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DB
    db_user: str = ""
    db_password: str = ""
    db_host: str = ""
    db_port: str = ""
    db_database: str = ""

    # RabbitMQ
    rabbitmq_host: str = ""
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "guest"
    rabbitmq_password: str = ""
    rabbitmq_vhost: str = "/"

    # JWT
    jwt_secret: str = ""

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_database}"
        )
    
    @property
    def database_url_migrations(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_database}"
        )

    @property
    def rabbitmq_url(self) -> str:
        return (
            f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}"
            f"@{self.rabbitmq_host}:{self.rabbitmq_port}/{self.rabbitmq_vhost}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings() 