from dataclasses import dataclass
from contexts.users.domain.value_objects.user_id import UserId
from contexts.users.domain.value_objects.full_name import FullName
from contexts.users.domain.value_objects.email import Email
from contexts.users.domain.value_objects.password import Password
from contexts.users.domain.value_objects.gender import Gender
from contexts.users.domain.value_objects.age import Age

@dataclass
class User:
    id: UserId
    full_name: FullName
    email: Email
    password: Password
    gender: Gender
    age: Age

    @staticmethod
    def create(full_name: FullName, email: Email, password: Password, gender: Gender, age: Age) -> "User":
        return User(
            id=UserId.new(),
            full_name=full_name,
            email=email,
            password=password,
            gender=gender,
            age=age
        )
