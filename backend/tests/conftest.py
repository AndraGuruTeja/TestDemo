
# import pytest
# import uuid
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.main import app
# from app.database import Base, get_db
# from app.models import WeatherRecord, User
# from app.config import settings
# import redis

# # Test database configuration
# TEST_DATABASE_URL = settings.DATABASE_URL
# engine = create_engine(
#     TEST_DATABASE_URL, 
#     connect_args={"check_same_thread": False}
# )

# TestingSessionLocal = sessionmaker(
#     autocommit=False, 
#     autoflush=False, 
#     bind=engine
# )

# @pytest.fixture(scope="session", autouse=True)
# def setup_database():
#     """
#     Fixture to create tables once before running all tests.
#     """
#     Base.metadata.create_all(bind=engine)  # Ensure tables are created before tests
#     yield

# @pytest.fixture(scope="function")
# def db_session():
#     """
#     Provides a database session for each test.
#     Uses SAVEPOINT for rollback without affecting other tests.
#     """
#     connection = engine.connect()
#     transaction = connection.begin()  # Start transaction
#     session = TestingSessionLocal(bind=connection)

#     try:
#         yield session  # Provide session to test
#     finally:
#         session.close()
#         transaction.rollback()  # Rollback instead of dropping tables
#         connection.close()


# @pytest.fixture
# def client(db_session):
#     """
#     Fixture to provide a FastAPI TestClient for testing endpoints.
#     Overrides the database dependency to use the test session.
#     """
#     def override_get_db():
#         try:
#             yield db_session
#         finally:
#             db_session.rollback()
    
#     app.dependency_overrides[get_db] = override_get_db
    
#     with TestClient(app) as test_client:
#         yield test_client

# @pytest.fixture
# def auth_header(client):
#     """
#     Fixture to provide an authentication header for authenticated requests.
#     Registers a unique test user and returns a valid JWT token.
#     """
#     username = f"test_{uuid.uuid4()}@example.com"
#     client.post("/register", json={"email": username, "password": "testpass"})

#     response = client.post(
#         "/token",
#         data={"username": username, "password": "testpass"}
#     )
#     return {"Authorization": f"Bearer {response.json()['access_token']}"}

# @pytest.fixture
# def mock_weather_api(monkeypatch):
#     """
#     Fixture to mock the external weather API response.
#     """
#     class MockResponse:
#         status_code = 200
        
#         @staticmethod
#         def json():
#             return {
#                 "name": "TestCity",
#                 "main": {"temp": 30.0, "humidity": 60},
#                 "weather": [{"description": "clear sky"}]
#             }
    
#     monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())

# @pytest.fixture(scope="session")
# def redis_client():
#     """
#     Fixture to provide a Redis client for the entire test session.
#     """
#     r = redis.Redis.from_url(settings.REDIS_URL)
#     yield r
#     r.close()

# @pytest.fixture(autouse=True)
# def clean_redis(redis_client):
#     """
#     Fixture to flush Redis before and after each test.
#     """
#     redis_client.flushall()
#     yield
#     redis_client.flushall()


# @pytest.fixture(autouse=True)
# def clean_tables(db_session):
#     """
#     Fixture to clean database tables before and after each test.
#     """
#     db_session.query(WeatherRecord).delete()
#     db_session.query(User).delete()
#     db_session.commit()
#     yield
#     db_session.query(WeatherRecord).delete()
#     db_session.query(User).delete()
#     db_session.commit()



import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.config import settings
from fastapi.testclient import TestClient

# Test database configuration for SQLite
TEST_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Fixture to create tables once before running all tests.
    """
    Base.metadata.create_all(bind=engine)
    yield

@pytest.fixture(scope="function")
def db_session():
    """
    Provides a database session for each test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def client(db_session):
    """
    Fixture to provide a FastAPI TestClient for testing endpoints.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.rollback()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client