from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User


async def insert_new_user(
    first_name: str,
    last_name: str,
    email: EmailStr,
    password_hash: bytes,
    salt: bytes,
    session: AsyncSession,
) -> User:
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=password_hash,
        salt=salt,
    )
    session.add(new_user)
    await session.commit()
    return new_user


async def get_user_by_email(
    email: EmailStr,
    session: AsyncSession,
) -> User | None:
    response = await session.execute(select(User).where(User.email == email))
    return response.scalar()


async def verify_user(
    token: str,
    session: AsyncSession,
) -> User | None:

    response = await session.execute(
        select(User).where(User.verification_token == token)
    )
    user = response.scalar()

    if user:
        user.verified = True
        await session.commit()
        return user


async def update_profile_picture(
    user_id: UUID,
    profile_picture: str,
    session: AsyncSession,
) -> User | None:

    response = await session.execute(select(User).where(User.id == user_id))
    user = response.scalar()

    if user:
        user.profile_picture = profile_picture
        await session.commit()
        return user
