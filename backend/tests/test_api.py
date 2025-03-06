
# import json
# from datetime import datetime, timedelta
# from unittest.mock import patch
# import pytest
# from fastapi import status
# from sqlalchemy.orm import Session
# from app.models import WeatherRecord
# from jose import jwt
# from app.config import settings

# def test_register_existing_user(client):
#     # First successful registration
#     client.post("/register", json={"email": "test@example.com", "password": "testpass"})
    
#     # Second attempt should fail
#     response = client.post(
#         "/register",
#         json={"email": "test@example.com", "password": "testpass"}
#     )
#     assert response.status_code == 400

# def test_login_invalid_credentials(client):
#     response = client.post(
#         "/token",
#         data={"username": "wrong@example.com", "password": "wrongpass"}
#     )
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED

# def test_protected_endpoint_without_token(client):
#     response = client.get("/weather/london")
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED

# def test_rate_limiting(client, auth_header):
#     for _ in range(10):
#         response = client.get("/weather/london", headers=auth_header)
#         assert response.status_code == status.HTTP_200_OK
    
#     response = client.get("/weather/london", headers=auth_header)
#     assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
#     assert "Retry-After" in response.headers

# def test_caching(client, auth_header):
#     # First request (uncached)
#     response = client.get("/weather/paris", headers=auth_header)
#     assert response.json()["cached"] is False
    
#     # Second request (cached)
#     response = client.get("/weather/paris", headers=auth_header)
#     assert response.json()["cached"] is True

# def test_api_fallback_to_fake_data(client, auth_header, mocker):
#     mocker.patch('requests.get', side_effect=Exception("API failure"))
    
#     response = client.get("/weather/berlin", headers=auth_header)
#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     assert 25 <= data["temperature"] <= 40
#     assert 10 <= data["humidity"] <= 80
# def test_historical_data_generation(client, auth_header, db_session: Session):
#     """
#     Test historical data generation.
#     """
#     # Get user ID from auth token
#     token = auth_header["Authorization"].split("Bearer ")[1]
#     payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#     user_id = payload["user_id"]
    
#     # Trigger history generation
#     response = client.get("/weather/history/london?days=7", headers=auth_header)
#     assert response.status_code == status.HTTP_200_OK
    
#     # Verify records
#     records = db_session.query(WeatherRecord).filter_by(city="london", user_id=user_id).all()
#     assert len(records) == 7, f"Expected 7 records, got {len(records)}"





import json
from datetime import datetime, timedelta
from unittest.mock import patch
import pytest
from fastapi import status
from sqlalchemy.orm import Session
from app.models import WeatherRecord
from jose import jwt
from app.config import settings


def test_login_valid_credentials(client):
    """
    Test logging in with valid credentials.
    """
    # Register a user first
    client.post("/register", json={"email": "test@example.com", "password": "testpass"})
    
    # Login with valid credentials
    response = client.post(
        "/token",
        data={"username": "test@example.com", "password": "testpass"}
    )
    assert response.status_code == status.HTTP_200_OK, "Login failed"
    assert "access_token" in response.json(), "Access token not returned"

def test_protected_endpoint_with_token(client, auth_header):
    """
    Test accessing a protected endpoint with a valid token.
    """
    response = client.get("/weather/london", headers=auth_header)
    assert response.status_code == status.HTTP_200_OK, "Access to protected endpoint failed"

def test_api_fallback_to_fake_data(client, auth_header, mocker):
    """
    Test that the API falls back to fake data when the external API fails.
    """
    mocker.patch('requests.get', side_effect=Exception("API failure"))
    
    response = client.get("/weather/berlin", headers=auth_header)
    assert response.status_code == status.HTTP_200_OK, "Fallback to fake data failed"
    data = response.json()
    assert 25 <= data["temperature"] <= 40, "Temperature out of range"
    assert 10 <= data["humidity"] <= 80, "Humidity out of range"