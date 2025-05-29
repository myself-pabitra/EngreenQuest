from functools import lru_cache
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, EmailStr, validator
from dotenv import load_dotenv
import os

# ✅ Load the .env file manually
load_dotenv(".env")


class Settings(BaseSettings):
    # -- Application --
    PROJECT_NAME: str = "Engreen Quest Contact API"
    API_V1_STR: str = "/api/v1"

    # -- Database --
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: int = 3306
    MYSQL_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @validator("SQLALCHEMY_DATABASE_URI", pre=True, always=True)
    def assemble_db_uri(cls, v, values):
        if v:
            return v
        user = values.get("MYSQL_USER")
        pw = values.get("MYSQL_PASSWORD")
        host = values.get("MYSQL_HOST")
        port = values.get("MYSQL_PORT")
        db = values.get("MYSQL_DB")
        return f"mysql+pymysql://{user}:{pw}@{host}:{port}/{db}?charset=utf8mb4"


@lru_cache
def get_settings() -> Settings:
    return Settings()
