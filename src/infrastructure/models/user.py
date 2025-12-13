from sqlalchemy.orm import Mapped, mapped_column

from src.domain.entities.user import User
from src.infrastructure.database import Base


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    username: Mapped[str] = mapped_column("username", nullable=True)
    fio: Mapped[str] = mapped_column("fio", nullable=False)
    phone_number: Mapped[str] = mapped_column("phone_number", nullable=False, unique=True)
    region: Mapped[str] = mapped_column("region", nullable=False)
    email: Mapped[str] = mapped_column("email", nullable=False)
    gender: Mapped[str] = mapped_column("gender", nullable=False)
    city: Mapped[str] = mapped_column("city", nullable=False)

    async def to_domain(self) -> User:
        return User(
            id=self.id,
            username=self.username,
            fio=self.fio,
            phone_number=self.phone_number,
            region=self.region,
            email=self.email,
            gender=self.gender,
            city=self.city
        )

    @classmethod
    async def from_domain(cls, user: User) -> 'UserORM':
        return cls(
            id=user.id,
            username=user.username,
            fio=user.fio,
            phone_number=user.phone_number,
            region=user.region,
            email=user.email,
            gender=user.gender,
            city=user.city
        )
