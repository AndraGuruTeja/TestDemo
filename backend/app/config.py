# # import os
# # from dotenv import load_dotenv

# # load_dotenv()

# # class Config:
# #     API_KEY = os.getenv("API_KEY")
# #     REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
# #     REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
# #     DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./weather.db")


# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     API_KEY = os.getenv("API_KEY")
#     REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
#     REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    
#     # Database configuration
#     DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./weather.db")  # Default to SQLite
#     if DATABASE_URL.startswith("postgresql"):
#         DATABASE_URL = DATABASE_URL.replace("postgresql", "postgresql+psycopg2")  # Use psycopg2 for PostgreSQL

#     # Authentication
#     SECRET_KEY = os.getenv("SECRET_KEY")
#     ALGORITHM = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES = 30

#     # Rate limiting
#     RATE_LIMIT = os.getenv("RATE_LIMIT", "5/minute")  # Default rate limit






























































































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