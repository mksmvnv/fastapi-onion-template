from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from models import Base
from utils.enums import UserRole
from utils.constants import (
    USERNAME_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
    NAME_MAX_LENGTH,
    PASSWORD_HASH_MAX_LENGTH,
)


class User(Base):
    username: Mapped[str] = mapped_column(
        String(USERNAME_MAX_LENGTH),
        unique=True,
        index=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(EMAIL_MAX_LENGTH),
        unique=True,
        index=True,
        nullable=False,
    )
    first_name: Mapped[str] = mapped_column(
        String(NAME_MAX_LENGTH), nullable=True
    )
    last_name: Mapped[str] = mapped_column(
        String(NAME_MAX_LENGTH), nullable=True
    )
    hashed_password: Mapped[str] = mapped_column(
        String(PASSWORD_HASH_MAX_LENGTH), nullable=False
    )
    role: Mapped[UserRole] = mapped_column(
        default=UserRole.USER, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
