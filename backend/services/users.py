from typing import List

from fastapi import HTTPException, status

from schemas import UserResponse, UserUpdate
from repositories.uow import AbstractUnitOfWork


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

    async def update_user(
        self, user_id: int, user_update: UserUpdate
    ) -> UserResponse:
        """
        Update a user by their ID.

        Args:
            user_id (int): The ID of the user to update.
            user_update (UserUpdate): The user update data.

        Returns:
            UserResponse: The updated user in response format.

        Raises:
            HTTPException: If the user is not found.
        """

        async with self.uow:
            user_data = user_update.model_dump()
            user = await self.uow.user_repository.update(user_id, user_data)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )
            await self.uow.commit()

            return UserResponse.model_validate(user)
