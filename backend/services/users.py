from uuid import UUID
from typing import List

from utils.uow import AbstractUnitOfWork
from schemas.users import UserResponse, UserUpdate, UserDeleteResponse
from utils.exceptions import UserNotFoundError, CredentialsAlreadyInUseError


class UserService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def get_user(self, user_id: UUID) -> UserResponse:
        async with self.uow:
            user = await self.uow.user_repository.get(user_id)
            if not user:
                raise UserNotFoundError
            return UserResponse.model_validate(user)

    async def get_users(self, page: int, limit: int) -> List[UserResponse]:
        async with self.uow:
            skip = (page - 1) * limit
            users = await self.uow.user_repository.list(skip, limit)
            if not users:
                raise UserNotFoundError
            return [UserResponse.model_validate(user) for user in users]

    async def update_user(self, user_update: UserUpdate) -> UserResponse:
        async with self.uow:
            if not await self.uow.user_repository.is_available(
                user_update.username, user_update.email
            ):
                raise CredentialsAlreadyInUseError
            user_data = user_update.model_dump(
                exclude_unset=True, exclude_none=True
            )
            user = await self.uow.user_repository.update(
                user_update.id, user_data
            )
            if not user:
                raise UserNotFoundError
            await self.uow.commit()
            return UserResponse.model_validate(user)

    async def delete_user(self, user_id: UUID):
        async with self.uow:
            deleted = await self.uow.user_repository.delete(user_id)
            if not deleted:
                raise UserNotFoundError
            await self.uow.commit()
            return UserDeleteResponse(id=user_id)
