
# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.orm import sessionmaker
# from .config import settings

# # Update the engine configuration to increase the connection pool size
# engine = create_engine(
#     settings.DATABASE_URL,
#     pool_size=20,  # Increase the pool size
#     max_overflow=30,  # Increase the overflow limit
#     pool_timeout=30,  # Timeout for acquiring a connection
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# Base = declarative_base()

# engine = create_engine(
#     settings.DATABASE_URL,
#     # Use a static pool for SQLite
# )




from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Configure database URL based on environment
if settings.DATABASE_TYPE == "sqlite":
    DATABASE_URL = settings.DATABASE_URL
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:  # PostgreSQL
    DATABASE_URL = settings.DATABASE_URL
    engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=30)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()