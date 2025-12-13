import logging

from sqlalchemy import select

from src.domain import exceptions
from src.domain.entities import User
from src.domain.interfaces import IUserRepository
from ..interfaces import IDatabaseUnitOfWork
from ..models.user import UserORM

logger = logging.getLogger(__name__)


class UserRepository(IUserRepository):
    __uow: IDatabaseUnitOfWork

    def __init__(self, uow: IDatabaseUnitOfWork):
        self.__uow = uow

    async def create_user(self, user: User) -> User:
        session = self.__uow.get_session()
        user_orm = await UserORM.from_domain(user)
        session.add(user_orm)
        await session.commit()
        await session.refresh(user_orm)
        return await user_orm.to_domain()

    async def get_user(self, user_id: int) -> User:
        logger.debug(f"Getting user by id={user_id}")
        session = self.__uow.get_session()
        stmt = select(UserORM).where(UserORM.id == user_id)
        user_orm = await session.scalar(stmt)
        if user_orm is None:
            logger.debug(f"Not found user with id={user_id}")
            raise exceptions.UserNotFoundError()
        logger.debug(f"Found user {user_orm.to_domain()}")
        return await user_orm.to_domain()

    async def is_phone_number_existing(self, phone_number: str) -> bool:
        session = self.__uow.get_session()
        stmt = select(UserORM).where(UserORM.phone_number == phone_number)
        user_orm = await session.scalar(stmt)
        logger.debug(user_orm)
        return user_orm is not None

    async def is_email_existing(self, email: str) -> bool:
        session = self.__uow.get_session()
        stmt = select(UserORM).where(UserORM.email == email)
        user_orm = await session.scalar(stmt)
        logger.debug(user_orm)
        return user_orm is not None
