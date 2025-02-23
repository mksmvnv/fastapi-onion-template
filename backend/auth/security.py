import jwt
import bcrypt

from datetime import datetime, timezone, timedelta

from fastapi.security import OAuth2PasswordBearer

from config import settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

public_key = settings.auth.public_key_path.read_text()
private_key = settings.auth.private_key_path.read_text()
algorithm = settings.auth.algorithm
access_token_expire_minutes = settings.auth.access_token_expire_minutes
refresh_token_expire_days = settings.auth.refresh_token_expire_days


def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(
        password.encode(), bcrypt.gensalt()
    ).decode()
    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_token(payload: dict, expires_delta: timedelta) -> str:
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded_jwt


def create_access_token(payload: dict) -> str:
    expires_delta = timedelta(minutes=access_token_expire_minutes)
    return create_token(payload, expires_delta)


def create_refresh_token(payload: dict) -> str:
    expires_delta = timedelta(days=refresh_token_expire_days)
    return create_token(payload, expires_delta)
