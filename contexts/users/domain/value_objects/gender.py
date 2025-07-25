from dataclasses import dataclass

@dataclass(frozen=True)
class Gender:
    value: str  # e.g. 'M', 'F', 'NB'

    def __post_init__(self):
        if self.value not in ('M', 'F', 'NB'):
            raise ValueError("Gender must be one of: M, F, NB")
