from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str | None
    fio: str
    phone_number: str
    region: str
    email: str