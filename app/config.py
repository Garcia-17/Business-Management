from pydantic import computed_field
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Businnes Management"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    PEFIX: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DATABASE: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr

    @computed_field
    @property
    def POSTGRES_CONNECTION_URL(self) -> str:
        return f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD.get_secret_value()}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DATABASE}"

    RESEND_API_KEY: SecretStr

    JWT_ACCESS_TOKEN_SECRET: SecretStr
    JWT_ACCESS_TOKEN_EXP_MINUTES: int
    JWT_REFRESH_TOKEN_SECRET: SecretStr
    JWT_REFRESH_TOKEN_EXP_DAYS: int

    S3_ENDPOINT: str
    S3_ACCESS_KEY_ID: str
    S3_ACCESS_KEY_SECRET: SecretStr
    S3_PROJECT_REGION: str


settings = Settings.settings_cached()


def get_settings() -> Settings:
    return settings
