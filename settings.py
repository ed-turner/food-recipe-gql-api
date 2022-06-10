from pydantic import BaseSettings, PostgresDsn, Field


class Settings(BaseSettings):
    """

    """

    DATABASE_URL: PostgresDsn = Field(env="DATABASE_URL")
