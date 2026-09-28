from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "PromptShield AI"
    ENV: str = "development"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    MONGODB_URI: str
    DATABASE_NAME: str

    REDIS_URL: str

    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()