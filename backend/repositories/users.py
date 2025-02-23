from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.users import UserLogin
from auth.security import verify_password
from repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(self.model).where(self.model.username == username)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(self.model).where(self.model.email == email)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def is_available(
        self, username: str | None, email: str | None
    ) -> bool:
        if username:
            if await self.get_by_username(username):
                return False
        if email:
            if await self.get_by_email(email):
                return False
        return True

    async def authenticate(self, user_login: UserLogin) -> User | None:
        user = await self.get_by_username(user_login.username)
        if not user:
            return None
        if not verify_password(
            user_login.password.get_secret_value(), user.hashed_password
        ):
            return None
        return user
