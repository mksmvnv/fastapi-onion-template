from utils.uow import AbstractUnitOfWork
from schemas.users import UserRegister, UserResponse
from auth.security import hash_password
from utils.exceptions import CredentialsAlreadyInUseError


class AuthService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def register(self, user_register: UserRegister) -> UserResponse:
        async with self.uow:
            if not await self.uow.user_repository.is_available(
                user_register.username, user_register.email
            ):
                raise CredentialsAlreadyInUseError
            hashed_password = hash_password(
                user_register.password.get_secret_value()
            )
            user_data = user_register.model_dump(
                exclude={"password", "confirm_password"},
                exclude_unset=True,
                exclude_none=True,
            )
            user_data["hashed_password"] = hashed_password
            user = await self.uow.user_repository.create(user_data)
            await self.uow.commit()
            return UserResponse.model_validate(user)
