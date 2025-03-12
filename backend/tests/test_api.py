
from fastapi import status
import pytest

def test_login_valid_credentials(client):
    """Test valid login credentials."""
    # Register test user
    client.post("/register", json={"email": "test@example.com", "password": "testpass"})
    
    # Login
    response = client.post("/token", data={"username": "test@example.com", "password": "testpass"})
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()

def test_invalid_token_rejection(client):
    """Test invalid JWT token rejection."""
    response = client.get("/weather/paris", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_missing_auth_header(client):
    """Test protected endpoint without auth header."""
    response = client.get("/weather/madrid")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "WWW-Authenticate" in response.headers
