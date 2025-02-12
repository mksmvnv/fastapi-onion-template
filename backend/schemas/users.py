from typing import Annotated
from annotated_types import Len
from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    PositiveInt,
    StrictStr,
    StrictBool,
    ConfigDict,
    model_validator,
)

from utils.constants import (
    USERNAME_MIN_LENGTH,
    USERNAME_MAX_LENGTH,
    NAME_MIN_LENGTH,
    NAME_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    PASSWORD_MAX_LENGTH,
)


UsernameStr = Annotated[str, Len(USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH)]
NameStr = Annotated[str, Len(NAME_MIN_LENGTH, NAME_MAX_LENGTH)]
PasswordStr = Annotated[
    SecretStr, Len(PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH)
]


class UserRegister(BaseModel):
    username: UsernameStr
    email: EmailStr
    first_name: NameStr | None = None
    last_name: NameStr | None = None
    password: PasswordStr
    confirm_password: PasswordStr

    @model_validator(mode="before")
    def verify_password_match(cls, values: dict) -> dict:
        password = values.get("password")
        confirm_password = values.get("confirm_password")

        if password != confirm_password:
            raise ValueError("The two passwords did not match.")
        return values


class UserResponse(BaseModel):
    id: PositiveInt
    username: UsernameStr
    email: EmailStr
    first_name: NameStr | None = None
    last_name: NameStr | None = None
    created_at: datetime
    updated_at: datetime
    role: StrictStr
    is_active: StrictBool

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    id: PositiveInt
    username: UsernameStr | None = None
    email: EmailStr | None = None
    first_name: NameStr | None = None
    last_name: NameStr | None = None

    @model_validator(mode="before")
    def check_fields(cls, values: dict) -> dict:
        if not any(
            [
                values.get("username"),
                values.get("email"),
                values.get("first_name"),
                values.get("last_name"),
            ]
        ):
            raise ValueError("At least one field must be provided.")
        return values
