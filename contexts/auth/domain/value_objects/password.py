from dataclasses import dataclass
import bcrypt

@dataclass(frozen=True)
class Password:
    value: str  # hashed password

    @staticmethod
    def hash_from_plain(plain_password: str) -> "Password":
        hashed = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())
        return Password(value=hashed.decode())

    def verify(self, plain_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), self.value.encode())
