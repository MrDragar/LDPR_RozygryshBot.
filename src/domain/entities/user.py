from dataclasses import dataclass
from datetime import date


@dataclass
class User:
    id: int
    username: str | None
    surname: str
    name: str
    patronymic: str
    birth_date: date
    phone_number: str
    region: str
    email: str
    gender: str
    city: str
