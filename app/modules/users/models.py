from datetime import datetime
from secrets import token_urlsafe
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, LargeBinary, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )

    first_name: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    verification_token: Mapped[str] = mapped_column(
        String(50), nullable=False, default=token_urlsafe(32)
    )

    profile_picture: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    password_hash: Mapped[bytes] = mapped_column(LargeBinary(16), nullable=False)

    salt: Mapped[bytes] = mapped_column(LargeBinary(16), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
