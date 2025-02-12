from typing import List

from fastapi import APIRouter, Query, status

from config import settings
from schemas.users import UserResponse, UserUpdate
from utils.dependencies import user_service_dep


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
async def get_user(
    user_id: int, user_service: user_service_dep
) -> UserResponse:
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        UserResponse: The user information in response format.

    Raises:
        HTTPException: If the user is not found.
    """

    user = await user_service.get_user(user_id)

    return user


@router.get(
    "/", response_model=List[UserResponse], status_code=status.HTTP_200_OK
)
async def get_users(
    user_service: user_service_dep,
    page: int = Query(
        settings.query.default_page, ge=settings.query.default_page
    ),
    limit: int = Query(
        settings.query.default_limit, le=settings.query.max_limit
    ),
) -> List[UserResponse]:
    """
    Retrieve a list of users.

    Args:
        page (int): The page to retrieve, 1-indexed.
        limit (int): The number of users to return per page.

    Returns:
        List[UserResponse]: A list of user information in response format.

    Raises:
        HTTPException: If no users are found.
    """

    users = await user_service.get_users(page, limit)

    return users


@router.patch(
    "/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
async def update_user(user_update: UserUpdate, user_service: user_service_dep):
    """
    Update a user's information by their ID.

    Args:
        user_update (UserUpdate): The user update data.

    Returns:
        UserResponse: The updated user in response format.

    Raises:
        HTTPException: If the user is not found or update fails.
    """

    user = await user_service.update_user(user_update)

    return user
