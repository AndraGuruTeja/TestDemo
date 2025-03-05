import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture(scope="module")
def auth_header(client):
    # Create test user
    client.post("/register", json={"email": "test@example.com", "password": "testpass"})
    
    # Get token
    response = client.post(
        "/token",
        data={"username": "test@example.com", "password": "testpass"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_weather(client, auth_header):
    response = client.get(
        "/weather/london",
        headers=auth_header
    )
    assert response.status_code == 200
    data = response.json()
    assert "temperature" in data
    assert "humidity" in data
    assert "description" in data

def test_get_history(client, auth_header):
    response = client.get(
        "/weather/history/london?days=7",
        headers=auth_header
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 7

def test_get_trends(client, auth_header):
    response = client.get(
        "/weather/trends/london?days=7",
        headers=auth_header
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("date" in item for item in data)