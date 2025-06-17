from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra="ignore")

    DATABASE_URL: str
    SYNC_DATABASE_URL: str
    TITLE: str
    DESCRIPTION: str
    ENV: str


settings = Settings()
