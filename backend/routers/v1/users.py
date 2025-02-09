from typing import List

from fastapi import APIRouter, Query, status

from schemas.v1.users import UserResponse
from utils.dependencies import user_service_dep
from utils.constants import DEFAULT_PAGE, DEFAULT_LIMIT, MAX_LIMIT


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
    page: int = Query(DEFAULT_PAGE, ge=DEFAULT_PAGE),
    limit: int = Query(DEFAULT_LIMIT, le=MAX_LIMIT),
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
