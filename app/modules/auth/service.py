from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from pydantic import EmailStr, SecretStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    generate_salt,
    generate_token,
    hash_password,
    verify_password,
)
from app.infraestructure.email.service import EmailService
from app.infraestructure.files.service import S3Service
from app.modules.users.repositories import (
    get_user_by_email,
    insert_new_user,
    verify_user,
)


async def sign_up(
    first_name: str,
    last_name: str,
    email: EmailStr,
    password: SecretStr,
    session: AsyncSession,
    email_service: EmailService,
):
    salt = generate_salt()
    password_hash = hash_password(password, salt)
    created_user = await insert_new_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=password_hash,
        salt=salt,
        session=session,
    )
    await email_service.send_verification_email(
        created_user.first_name, created_user.email, created_user.verification_token
    )
    return created_user


async def verify_email(
    token: str,
    session: AsyncSession,
):
    return await verify_user(token, session)


async def login(
    email: EmailStr,
    password: SecretStr,
    access_token_secret: SecretStr,
    access_token_exp_minutes: int,
    refresh_token_secret: SecretStr,
    refresh_token_exp_days: int,
    session: AsyncSession,
    s3_service: S3Service,
):

    user = await get_user_by_email(email, session)

    if not user:
        raise HTTPException(401, "User not found")

    provided_password_hash = hash_password(password, user.salt)

    password_match = verify_password(user.password_hash, provided_password_hash)

    if not password_match:
        raise HTTPException(401, "Contraseña incorrecta")

    now = datetime.now(UTC)

    access_token_exp = now + timedelta(minutes=access_token_exp_minutes)

    access_token = generate_token(
        {
            "user_id": str(user.id),
            "email": email,
            "profile_picture": str(user.profile_picture),
            "exp": access_token_exp.timestamp(),
        },
        access_token_secret,
    )

    refresh_token_exp = now + timedelta(days=refresh_token_exp_days)

    refresh_token = generate_token(
        {
            "user_id": str(user.id),
            "email": email,
            "profile_picture": str(user.profile_picture),
            "exp": refresh_token_exp.timestamp(),
        },
        refresh_token_secret,
    )

    return (
        access_token,
        access_token_exp.timestamp(),
        refresh_token,
        refresh_token_exp.timestamp(),
    )
