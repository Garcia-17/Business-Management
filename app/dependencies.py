from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.core.security import decode_token
from app.database.session import get_db
from app.infraestructure.email.service import EmailService
from app.infraestructure.files.service import S3Service
from app.modules.users.models import User

SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_email_service(request: Request) -> EmailService:
    return request.app.state.email_service


EmailServiceDep = Annotated[EmailService, Depends(get_email_service)]


def get_s3_service(request: Request) -> S3Service:
    return request.app.state.s3_service


S3ServiceDep = Annotated[S3Service, Depends(get_s3_service)]


SettingsDep = Annotated[Settings, Depends(get_settings)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{get_settings().PEFIX}/auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     try:
#         payload = decode_token(token, get_settings().JWT_ACCESS_TOKEN_SECRET)
#         username = payload.get("user_id")
#         if username is None:
#             raise credentials_exception
#     except InvalidTokenError:
#         raise credentials_exception
#     return UserSchema(**payload)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: SessionDep,
):

    try:
        payload = decode_token(
            token,
            get_settings().JWT_ACCESS_TOKEN_SECRET,
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        user_id = UUID(user_id)

    except (InvalidTokenError, ValueError, TypeError):
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == user_id))

    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception
    return user


UserDep = Annotated[User, Depends(get_current_user)]
