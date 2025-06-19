from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_ignore_empty=True
    )

    DATABASE_URL: str
    SYNC_DATABASE_URL: str
    TITLE: str
    DESCRIPTION: str
    ENV: str
    ADMIN: str
    ADMIN_PASSWORD: str
    ADMIN_USERNAME: str
    SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


settings = Settings()
