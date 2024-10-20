import logging
from secret_key_generator import secret_key_generator
from functools import lru_cache
from typing import Any, Union
from pydantic import field_validator, ValidationInfo, EmailStr, PostgresDsn
from pydantic_settings import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Main Service"

    # Use this to periodically generate secret at a python cli
    # SECRET_KEY = secret_key_generator.generate(len_of_secret_key=64, file_name=".secret.txt")
    # print(SECRET_KEY)
    # SECRET_KEY: str = "(a8hhjkk-_sm-(9nsn7wo$v%9y^n96*gixb@hc6^ft6&8hg6sdm!)&2odhld(p$m"

    SECRET_KEY: Union[str, None] = None

    @field_validator("SECRET_KEY")
    def create_test_env(cls, v: str, info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return info.data["SECRET_KEY"]

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URL: Union[str, None] = None

    @field_validator("SQLALCHEMY_DATABASE_URL")
    def assemble_db_connection(cls, v: str, info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        # SQLALCHEMY_DATABASE_URL = "postgresql://postgres:changethis@db:5432/microservices_db"
        conn_url = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data["POSTGRES_USER"],
            password=info.data["POSTGRES_PASSWORD"],
            host=info.data["POSTGRES_SERVER"],
            path=f"{info.data['POSTGRES_DB']}",
        )
        return str(conn_url)

    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3
    ACTIVATION_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8


@lru_cache()
def get_settings() -> Settings:
    log.info("loading config settings from the .env...")
    return Settings()
