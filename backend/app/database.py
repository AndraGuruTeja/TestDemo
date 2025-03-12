


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings  # Ensure correct relative import

Base = declarative_base()

DATABASE_URL = settings.DATABASE_URL

# PostgreSQL Engine
engine = create_engine(
    DATABASE_URL,
    pool_size=30,
    max_overflow=30,
    pool_timeout=30,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from . import models  # Import models after Base definition
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
print(f"Using DATABASE_URL: {DATABASE_URL}")