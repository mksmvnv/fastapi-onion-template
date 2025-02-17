from fastapi import APIRouter, status

from schemas.users import UserRegister, UserResponse
from utils.dependencies import auth_service_dep


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_register: UserRegister, auth_service: auth_service_dep
) -> UserResponse:
    user = await auth_service.register(user_register)
    return user
