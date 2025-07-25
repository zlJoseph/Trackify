import pytest # type: ignore
from uuid import UUID
from contexts.users.domain.entities.user import User
from contexts.users.domain.value_objects.full_name import FullName
from contexts.users.domain.value_objects.email import Email
from contexts.users.domain.value_objects.password import Password
from contexts.users.domain.value_objects.gender import Gender
from contexts.users.domain.value_objects.age import Age

def test_create_user_successfully():
    # Arrange
    full_name = FullName(first_name="José", last_name="Vegas", middle_name="Carrillo")
    email = Email("jose@example.com")
    password = Password.hash_from_plain("Probando@1")
    gender = Gender("M")
    age = Age(25)

    # Act
    user = User.create(full_name, email, password, gender, age)

    # Assert
    assert user.id is not None
    assert isinstance(user.id.value, UUID)
    assert user.full_name == full_name
    assert user.email == email
    assert user.password.value != "Probando@1"
    assert user.gender == gender
    assert user.age.value == 25


def test_valid_email():
    email = Email("test@example.com")
    assert email.value == "test@example.com"

def test_invalid_email():
    with pytest.raises(ValueError):
        Email("not-an-email")

def test_valid_age():
    age = Age(30)
    assert age.value == 30

def test_invalid_age_negative():
    with pytest.raises(ValueError):
        Age(-5)

def test_password_hashing():
    plain_password = "Probando@1"
    password = Password.hash_from_plain(plain_password)
    assert password.value != plain_password
    assert password.verify(plain_password) is True


def test_password_verification_fails():
    password = Password.hash_from_plain("Probando@1")
    assert password.verify("wrongpassword") is False