from dataclasses import dataclass
import bcrypt
from contexts.users.domain.exceptions.invalid_password_exception import InvalidPasswordException

@dataclass(frozen=True)
class Password:
    value: str  # hashed password

    @staticmethod
    def hash_from_plain(plain_password: str) -> "Password":
        if not (8 <= len(plain_password) <= 64):
            raise InvalidPasswordException("La contraseña debe tener entre 8 y 64 caracteres.")

        if not Password._has_complexity(plain_password):
            raise InvalidPasswordException(
                "Debe contener mayúsculas, minúsculas, números y símbolos."
            )
        hashed = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())
        return Password(value=hashed.decode())

    @staticmethod
    def _has_complexity(password: str) -> bool:
        import re
        return all([
            bool(re.search(r"[A-Z]", password)),
            bool(re.search(r"[a-z]", password)),
            bool(re.search(r"[0-9]", password)),
            bool(re.search(r"[\W_]", password)),
        ])

    def verify(self, plain_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), self.value.encode())
