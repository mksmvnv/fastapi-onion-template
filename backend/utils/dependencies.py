from typing import Annotated

from fastapi import Depends

from services.auth import AuthService
from services.users import UserService
from utils.uow import AbstractUnitOfWork, UnitOfWork


UOFDep = Annotated[AbstractUnitOfWork, Depends(UnitOfWork)]


def get_auth_service(uow: UOFDep) -> AuthService:
    return AuthService(uow)


def get_user_service(uow: UOFDep) -> UserService:
    return UserService(uow)


auth_service_dep = Annotated[AuthService, Depends(get_auth_service)]
user_service_dep = Annotated[UserService, Depends(get_user_service)]
