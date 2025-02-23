from fastapi import APIRouter, status

from schemas.tokens import TokenResponse
from schemas.users import UserRegister, UserResponse, UserLogin
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


@router.post(
    "/login", response_model=TokenResponse, status_code=status.HTTP_200_OK
)
async def login(
    user_login: UserLogin, auth_service: auth_service_dep
) -> TokenResponse:
    user = await auth_service.login(user_login)
    return user
