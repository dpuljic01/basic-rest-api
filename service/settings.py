import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = os.getenv(
        "SQLALCHEMY_DATABASE_URL", "sqlite+aiosqlite:///./dates_db.db"
    )
    NUMBERS_API_BASE_URL: str = "http://numbersapi.com"
    NUMBERS_API_KEY: str = os.getenv("NUMBERS_API_KEY", "SECRET_API_KEY")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
