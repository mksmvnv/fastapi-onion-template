from abc import ABC, abstractmethod

from database import async_session_maker
from repositories.users import UserRepository


class AbstractUnitOfWork(ABC):
    user_repository: UserRepository

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        """
        Create a new session and set up the repositories.

        On entering the context, a new session is created and the
        repositories are set up with this session.
        """

        self.session = self.session_factory()

        # Repositories
        self.user_repository = UserRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
