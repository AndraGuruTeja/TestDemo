
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from .config import settings

# # Configure database URL based on environment
# if settings.DATABASE_TYPE == "sqlite":
  
#     DATABASE_URL = settings.DATABASE_URL
#     engine = create_engine(
#         DATABASE_URL, 
#         connect_args={"check_same_thread": False},
        
#         pool_size=20,  # Increase the pool size
#         max_overflow=30,  # Increase the overflow limit
#         pool_timeout=30,  # Timeout for acquiring a connection
#         pool_recycle=3600  # Recycle connections after 1 hour
#     )

# else:  # PostgreSQL
#     DATABASE_URL = settings.DATABASE_URL
#     engine = create_engine(DATABASE_URL, pool_size=30, max_overflow=30)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
# print(f"Using DATABASE_URL: {DATABASE_URL}")
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()





from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Configure database URL for SQLite
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    pool_size=20,
    max_overflow=30,
    pool_timeout=30,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()