from typing import Annotated

from fastapi import Depends

from services.auth import AuthService
from services.users import UserService
from utils.uow import AbstractUnitOfWork, UnitOfWork


UOFDep = Annotated[AbstractUnitOfWork, Depends(UnitOfWork)]


def get_auth_service(uow: UOFDep) -> AuthService:
    """
    Dependency injection for AuthService.

    Args:
        uow (UOFDep): The unit of work dependency.

    Returns:
        AuthService: An instance of AuthService initialized with the
        provided unit of work.
    """

    return AuthService(uow)


def get_user_service(uow: UOFDep) -> UserService:
    """
    Dependency injection for UserService.

    Args:
        uow (UOFDep): The unit of work dependency.

    Returns:
        UserService: An instance of UserService initialized with the
        provided unit of work.
    """

    return UserService(uow)


auth_service_dep = Annotated[AuthService, Depends(get_auth_service)]
user_service_dep = Annotated[UserService, Depends(get_user_service)]
