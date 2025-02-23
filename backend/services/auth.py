from utils.uow import AbstractUnitOfWork
from schemas.tokens import TokenResponse
from schemas.users import UserRegister, UserLogin, UserResponse
from auth.security import (
    hash_password,
    create_access_token,
    create_refresh_token,
)
from utils.exceptions import (
    CredentialsAlreadyInUseError,
    InvalidCredentialsError,
)


class AuthService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def register(self, user_register: UserRegister) -> UserResponse:
        # Хешируем до транзакции
        hashed_password = hash_password(
            user_register.password.get_secret_value()
        )

        async with self.uow:
            if not await self.uow.user_repository.is_available(
                user_register.username, user_register.email
            ):
                raise CredentialsAlreadyInUseError
            user_data = user_register.model_dump(
                exclude={"password", "confirm_password"},
                exclude_unset=True,
                exclude_none=True,
            )
            user_data["hashed_password"] = hashed_password
            user = await self.uow.user_repository.create(user_data)
            await self.uow.commit()
            return UserResponse.model_validate(user)

    async def login(self, user_login: UserLogin) -> TokenResponse:
        async with self.uow:
            user = await self.uow.user_repository.authenticate(user_login)
            if not user:
                raise InvalidCredentialsError
            access_token_payload = {
                "sub": str(user.id),
                "username": user.username,
                "role": user.role,
                "is_active": user.is_active,
            }
            refresh_token_payload = {
                "sub": str(user.id),
                "username": user.username,
            }
            access_token = create_access_token(access_token_payload)
            refresh_token = create_refresh_token(refresh_token_payload)
            return TokenResponse(
                access_token=access_token, refresh_token=refresh_token
            )
