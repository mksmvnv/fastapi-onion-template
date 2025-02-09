from fastapi import APIRouter, status

from utils.dependencies import auth_service_dep
from schemas.v1.users import UserRegister, UserResponse


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
    """
    Registers a new user.

    Args:
        user_register (UserRegister): The user registration data.

    Returns:
        UserResponse: The registered user in response format.

    Raises:
        HTTPException: If the credentials are already in use
            or the passwords do not match.
    """

    user = await auth_service.register(user_register)

    return user
