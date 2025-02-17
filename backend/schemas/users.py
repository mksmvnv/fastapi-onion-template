from uuid import UUID
from typing import Annotated
from annotated_types import Len
from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    StrictStr,
    StrictBool,
    ConfigDict,
    model_validator,
    field_validator,
)

from utils.exceptions import (
    PasswordsDoNotMatchError,
    AtLeastOneFieldIsRequiredError,
)


UsernameStr = Annotated[StrictStr, Len(min_length=2, max_length=16)]
NameStr = Annotated[StrictStr, Len(min_length=1, max_length=96)]
PasswordStr = Annotated[SecretStr, Len(min_length=8, max_length=255)]


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
            raise PasswordsDoNotMatchError
        return values


class UserResponse(BaseModel):
    id: UUID
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
    id: UUID
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
            raise AtLeastOneFieldIsRequiredError
        return values


class UserDeleteResponse(BaseModel):
    id: UUID
    status: StrictStr = "deleted"
