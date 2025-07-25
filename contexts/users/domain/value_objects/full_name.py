from dataclasses import dataclass

@dataclass(frozen=True)
class FullName:
    first_name: str
    last_name: str
    middle_name: str

    def full(self) -> str:
        return f"{self.first_name} {self.last_name} {self.middle_name}".strip()
