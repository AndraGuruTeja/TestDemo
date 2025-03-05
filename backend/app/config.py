
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./weather.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    OPENWEATHER_API_KEY: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    
    class Config:
        env_file = ".env"

settings = Settings()