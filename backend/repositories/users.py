from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_username(self, username: str) -> User | None:
        """
        Retrieve a user by their username.

        Args:
        username (str): The username to be retrieved.

        Returns:
        User | None: The user with the given username or None if not found.
        """

        stmt = select(self.model).where(self.model.username == username)
        res = await self.session.execute(stmt)

        return res.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email.

        Args:
        email (str): The email of the user to be retrieved.

        Returns:
        User | None: The user with the given email or None if not found.
        """

        stmt = select(self.model).where(self.model.email == email)
        res = await self.session.execute(stmt)

        return res.scalar_one_or_none()

    async def is_available(
        self, username: str | None, email: str | None
    ) -> bool:
        """
        Checks if the given username and/or email is available.

        Args:
        username (str | None): The username to check.
        email (str | None): The email to check.

        Returns:
        bool: True if the given username and/or email is available,
            otherwise False.
        """

        if username:
            if await self.get_by_username(username):
                return False

        if email:
            if await self.get_by_email(email):
                return False

        return True
