from abc import ABC, abstractmethod
from contextlib import _AsyncGeneratorContextManager

from .entities import User


class IUnitOfWork(ABC):
    @abstractmethod
    def atomic(self) -> _AsyncGeneratorContextManager[None, None]:
        ...


class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        ...

    @abstractmethod
    async def get_user(self, user_id: int) -> User:
        ...

    @abstractmethod
    async def is_phone_number_existing(self, phone_number: str) -> bool:
        ...
    
    @abstractmethod
    async def is_email_existing(self, email: str) -> bool:
        ...

    @abstractmethod
    async def get_users(
        self, 
        skip: int = 0, 
        limit: int = 100,
        **filters
    ) -> list[User]:
        ...


class IStringSorterRepository(ABC):
    @abstractmethod
    async def sort_by_similarity(self, target: str, string_list: list[str]) -> list[str]:
        ...
