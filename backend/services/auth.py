from fastapi import HTTPException, status

from utils.uow import AbstractUnitOfWork
from schemas.v1.users import UserRegister, UserResponse
from auth.hash import hash_password


class AuthService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def register(self, user_register: UserRegister) -> UserResponse:
        """
        Registers a new user and returns the registered user
        in a response format.

        Args:
            user_register (UserRegister): The user registration data.

        Returns:
            UserResponse: The registered user in response format.

        Raises:
            HTTPException: If the credentials are already in use
                or the passwordsdo not match.
        """

        async with self.uow:
            if not await self.uow.user_repository.is_available(
                user_register.username, user_register.email
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Credentials already in use",
                )
            if user_register.password != user_register.confirm_password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Passwords do not match",
                )

            hashed_password = hash_password(
                user_register.password.get_secret_value()
            )
            user_data = user_register.model_dump(
                exclude={"password", "confirm_password"},
            )
            user_data["hashed_password"] = hashed_password
            user = await self.uow.user_repository.create(user_data)
            await self.uow.commit()

            return UserResponse.model_validate(user)
