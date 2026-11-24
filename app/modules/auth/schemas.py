from uuid import UUID

from pydantic import BaseModel, EmailStr, Field
from pydantic.types import SecretStr


class SignUpEntry(BaseModel):
    first_name: str = Field(min_length=1, max_length=25)
    last_name: str = Field(min_length=1, max_length=25)
    email: EmailStr = Field(min_length=1, max_length=50)
    password: SecretStr = Field(min_length=1, max_length=50)


class SignUpOutput(BaseModel):
    success: bool = True
    user_id: UUID = Field(alias="id")


class VerifyOutput(BaseModel):
    success: bool = True
    user_id: UUID = Field(alias="id")


class LoginEntry(BaseModel):
    email: EmailStr = Field(min_length=1, max_length=50)
    password: SecretStr = Field(min_length=1, max_length=50)


class LoginOutput(BaseModel):
    access_token: str
    access_token_exp_at: float
    refresh_token: str
    refresh_token_exp_at: float
