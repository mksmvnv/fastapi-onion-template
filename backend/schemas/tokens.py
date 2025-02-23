from uuid import UUID
from typing import Annotated
from annotated_types import Len

from pydantic import BaseModel, StrictStr, StrictBool, StrictInt


UsernameStr = Annotated[StrictStr, Len(min_length=2, max_length=16)]


class AccessTokenPayload(BaseModel):
    sub: UUID
    username: UsernameStr
    role: StrictStr
    is_active: StrictBool
    token_type: StrictStr = "access"
    exp: StrictInt
    iat: StrictInt


class RefreshTokenPayload(BaseModel):
    sub: UUID
    username: UsernameStr
    token_type: StrictStr = "refresh"
    exp: StrictInt
    iat: StrictInt


class TokenResponse(BaseModel):
    access_token: StrictStr
    refresh_token: StrictStr
    token_type: StrictStr = "bearer"
