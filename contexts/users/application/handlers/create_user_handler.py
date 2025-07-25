from shared.domain.events.event_bus import EventBus
from contexts.users.domain.repositories.user_repository import UserRepository
from contexts.users.domain.value_objects.full_name import FullName
from contexts.users.domain.value_objects.email import Email
from contexts.users.domain.value_objects.password import Password
from contexts.users.domain.value_objects.gender import Gender
from contexts.users.domain.value_objects.age import Age
from contexts.users.domain.entities.user import User
from contexts.users.application.commands.create_user import CreateUserCommand
from contexts.users.application.events.user_created import UserCreatedEvent


class CreateUserHandler:
    def __init__(self, user_repo: UserRepository, event_bus: EventBus):
        self.user_repo = user_repo
        self.event_bus = event_bus

    async def handle(self, command: CreateUserCommand) -> None:
        full_name = FullName(
            first_name=command.first_name,
            last_name=command.last_name,
            middle_name=command.middle_name
        )

        email = Email(command.email)
        gender = Gender(command.gender)
        age = Age(command.age)

        user = User.create(full_name, email, Password.hash_from_plain(command.password), gender, age)

        await self.user_repo.save(user)

        event = UserCreatedEvent(
            user_id=user.id.value,
            email=user.email.value,
            password=user.password.value,
            full_name=user.full_name,
            gender=user.gender.value,
            age=user.age.value
        )

        await self.event_bus.publish(event)
