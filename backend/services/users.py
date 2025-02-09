from typing import List

from fastapi import HTTPException, status

from utils.uow import AbstractUnitOfWork
from schemas.v1.users import UserResponse


class UserService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def get_user(self, user_id: int) -> UserResponse:
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            UserResponse: The user information in response format.

        Raises:
            HTTPException: If the user is not found.
        """

        async with self.uow:
            user = await self.uow.user_repository.get(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )

            return UserResponse.model_validate(user)

    async def get_users(self, page: int, limit: int) -> List[UserResponse]:
        """
        Retrieve a list of users with pagination.

        Args:
            page (int): The page number to retrieve, 1-indexed.
            limit (int): The number of users to return per page.

        Returns:
            List[UserResponse]: A list of user information in response format.

        Raises:
            HTTPException: If no users are found.
        """

        async with self.uow:
            skip = (page - 1) * limit
            users = await self.uow.user_repository.list(skip, limit)
            if not users:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Users not found",
                )

            return [UserResponse.model_validate(user) for user in users]
