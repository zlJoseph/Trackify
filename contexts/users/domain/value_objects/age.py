from dataclasses import dataclass

@dataclass(frozen=True)
class Age:
    value: int

    def __post_init__(self):
        if self.value < 0 or self.value > 120:
            raise ValueError("Invalid age")
