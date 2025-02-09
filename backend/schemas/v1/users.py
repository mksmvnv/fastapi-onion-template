from typing import Annotated
from annotated_types import Len

from datetime import datetime

from pydantic import BaseModel, EmailStr, SecretStr, ConfigDict

from utils.constants import (
    USERNAME_MIN_LEN,
    USERNAME_MAX_LEN,
    PASSWORD_MIN_LEN,
    PASSWORD_MAX_LEN,
)


UsernameStr = Annotated[str, Len(USERNAME_MIN_LEN, USERNAME_MAX_LEN)]
PasswordStr = Annotated[SecretStr, Len(PASSWORD_MIN_LEN, PASSWORD_MAX_LEN)]


class UserRegister(BaseModel):
    username: UsernameStr
    email: EmailStr
    password: PasswordStr
    confirm_password: PasswordStr


class UserResponse(BaseModel):
    id: int
    username: UsernameStr
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: UsernameStr
    email: EmailStr
