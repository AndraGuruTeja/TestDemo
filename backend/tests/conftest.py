
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.config import settings
from fastapi.testclient import TestClient

# Use the PostgreSQL database URL from .env
TEST_DATABASE_URL = settings.DATABASE_URL  # Ensure this points to PostgreSQL
print(f"Using TEST_DATABASE_URL: {TEST_DATABASE_URL}")

# Create engine for PostgreSQL
engine = create_engine(TEST_DATABASE_URL)

# Create a session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Fixture to create tables if they do not exist before running tests.
    Does NOT delete existing tables.
    """
    Base.metadata.create_all(bind=engine)  # Ensures missing tables are created
    yield

@pytest.fixture(scope="function")
def db_session():
    """
    Provides a database session for each test.
    Uses a transaction to rollback after each test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()  # Rollback changes made during test
        connection.close()

@pytest.fixture
def client(db_session):
    """
    Provides a FastAPI TestClient for testing endpoints.
    Overrides get_db to use the test session.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.rollback()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
