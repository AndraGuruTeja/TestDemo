

import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_TYPE: str = os.getenv("DATABASE_TYPE")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

    class Config:
        env_file = ".env"

settings = Settings()
