from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column

from models import Base
from utils.enums import UserRole


class User(Base):
    username: Mapped[str] = mapped_column(
        String(16), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(96), nullable=True)
    last_name: Mapped[str] = mapped_column(String(96), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), default=UserRole.USER, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
