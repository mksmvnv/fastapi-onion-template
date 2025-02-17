from uuid import UUID
from typing import List

from fastapi import APIRouter, Query, status

from config import settings
from schemas.users import UserResponse, UserUpdate, UserDeleteResponse
from utils.dependencies import user_service_dep


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
async def get_user(
    user_id: UUID, user_service: user_service_dep
) -> UserResponse:
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
    users = await user_service.get_users(page, limit)
    return users


@router.patch(
    "/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
async def update_user(
    user_update: UserUpdate, user_service: user_service_dep
) -> UserResponse:
    user = await user_service.update_user(user_update)
    return user


@router.delete(
    "/{user_id}",
    response_model=UserDeleteResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    user_id: UUID, user_service: user_service_dep
) -> UserDeleteResponse:
    deleted_user = await user_service.delete_user(user_id)
    return deleted_user
