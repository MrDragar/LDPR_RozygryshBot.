from dataclasses import dataclass, field
from datetime import date, datetime


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
    created_at: datetime = field(default_factory=lambda: datetime.now())
