from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr, ValidationError

from app.dependencies import EmailServiceDep, S3ServiceDep, SessionDep, SettingsDep
from app.modules.auth.schemas import (
    LoginEntry,
    LoginOutput,
    SignUpEntry,
    SignUpOutput,
    VerifyOutput,
)
from app.modules.auth.service import login, sign_up, verify_email

auth_router = APIRouter(tags=["Auth"])


@auth_router.post("/sign_up", response_model=SignUpOutput)
async def _sign_up(
    data: SignUpEntry, session: SessionDep, email_service: EmailServiceDep
):
    return await sign_up(
        **data.model_dump(), session=session, email_service=email_service
    )


@auth_router.get("/verify", response_model=VerifyOutput)
async def _verify(token: str, session: SessionDep):
    return await verify_email(token=token, session=session)


@auth_router.post("/login")
async def _login(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
    settings: SettingsDep,
    s3_service: S3ServiceDep,
):
    try:
        clean_data = LoginEntry(email=data.username, password=SecretStr(data.password))
    except ValidationError as ex:
        raise HTTPException(400, str(ex))

    (
        access_token,
        access_token_exp_at,
        refresh_token,
        refresh_token_exp_at,
    ) = await login(
        clean_data.email,
        clean_data.password,
        settings.JWT_ACCESS_TOKEN_SECRET,
        settings.JWT_ACCESS_TOKEN_EXP_MINUTES,
        settings.JWT_REFRESH_TOKEN_SECRET,
        settings.JWT_REFRESH_TOKEN_EXP_DAYS,
        session,
        s3_service,
    )

    return LoginOutput(
        access_token=access_token,
        access_token_exp_at=access_token_exp_at,
        refresh_token=refresh_token,
        refresh_token_exp_at=refresh_token_exp_at,
    )


@auth_router.post("/logout")
async def _logout():
    return ""
