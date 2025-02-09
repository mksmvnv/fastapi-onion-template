from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base import BaseRepository
from models.users import User


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

    async def is_available(self, username: str, email: str) -> bool:
        """
        Check if a given username and email are available.

        Args:
            username (str): The username to be checked.
            email (str): The email to be checked.

        Returns:
            bool: True if the username and email are available,
            False otherwise.
        """

        if await self.get_by_username(username) or await self.get_by_email(
            email
        ):
            return False

        return True
