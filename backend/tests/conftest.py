


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
# TEST_DATABASE_URL = "sqlite:///:memory:"
# engine = create_engine(
#     TEST_DATABASE_URL, 
#     connect_args={"check_same_thread": False}
# )
# TestingSessionLocal = sessionmaker(
#     autocommit=False, 
#     autoflush=False, 
#     bind=engine
# )

# @pytest.fixture(scope="function")
# def db_session():
#     """
#     Fixture to provide a database session for each test.
#     Creates and drops tables for each test to ensure isolation.
#     """
#     # Create tables
#     Base.metadata.create_all(bind=engine)
    
#     # Start transaction
#     connection = engine.connect()
#     transaction = connection.begin()
#     session = TestingSessionLocal(bind=connection)
    
#     yield session
    
#     # Rollback transaction and clean up
#     session.close()
#     transaction.rollback()
#     connection.close()
#     Base.metadata.drop_all(bind=engine)

# @pytest.fixture
# def client(db_session):
#     """
#     Fixture to provide a FastAPI TestClient for testing endpoints.
#     Overrides the database dependency to use the test session.
#     """
#     # Dependency override
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
#     # Generate unique test user
#     username = f"test_{uuid.uuid4()}@example.com"
#     client.post("/register", json={
#         "email": username,
#         "password": "testpass"
#     })
    
#     # Get auth token
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
    
#     # Mock requests.get
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
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import WeatherRecord, User
from app.config import settings
import redis

# Test database configuration
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)
@pytest.fixture(scope="function")
def db_session():
    """
    Fixture to provide a database session for each test.
    Creates and drops tables for each test to ensure isolation.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Start transaction
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    # Clean up and close resources
    session.close()
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    """
    Fixture to provide a FastAPI TestClient for testing endpoints.
    Overrides the database dependency to use the test session.
    """
    # Dependency override
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.rollback()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def auth_header(client):
    """
    Fixture to provide an authentication header for authenticated requests.
    Registers a unique test user and returns a valid JWT token.
    """
    # Generate unique test user
    username = f"test_{uuid.uuid4()}@example.com"
    client.post("/register", json={
        "email": username,
        "password": "testpass"
    })
    
    # Get auth token
    response = client.post(
        "/token",
        data={"username": username, "password": "testpass"}
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}

@pytest.fixture
def mock_weather_api(monkeypatch):
    """
    Fixture to mock the external weather API response.
    """
    class MockResponse:
        status_code = 200
        
        @staticmethod
        def json():
            return {
                "name": "TestCity",
                "main": {"temp": 30.0, "humidity": 60},
                "weather": [{"description": "clear sky"}]
            }
    
    # Mock requests.get
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())

@pytest.fixture(scope="session")
def redis_client():
    """
    Fixture to provide a Redis client for the entire test session.
    """
    r = redis.Redis.from_url(settings.REDIS_URL)
    yield r
    r.close()

@pytest.fixture(autouse=True)
def clean_redis(redis_client):
    """
    Fixture to flush Redis before and after each test.
    """
    redis_client.flushall()
    yield
    redis_client.flushall()

@pytest.fixture(autouse=True)
def clean_tables(db_session):
    """
    Fixture to clean database tables before and after each test.
    """
    db_session.query(WeatherRecord).delete()
    db_session.query(User).delete()
    db_session.commit()
    yield
    db_session.query(WeatherRecord).delete()
    db_session.query(User).delete()
    db_session.commit()