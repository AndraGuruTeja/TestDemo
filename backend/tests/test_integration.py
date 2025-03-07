
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.data import generate_history, get_current_time, generate_fake_weather_data
from app.models import WeatherRecord
from unittest.mock import patch

def test_get_current_time():
    """
    Test that `get_current_time` returns a datetime object.
    """
    current_time = get_current_time()
    assert isinstance(current_time, datetime), "Expected a datetime object"

def test_generate_fake_weather_data():
    """
    Test that `generate_fake_weather_data` returns valid weather data.
    """
    city = "test_city"
    weather_data = generate_fake_weather_data(city)
    
    # Check required fields
    assert weather_data["city"] == city, f"Expected city to be {city}"
    assert 25 <= weather_data["temperature"] <= 40, "Temperature out of range"
    assert 10 <= weather_data["humidity"] <= 80, "Humidity out of range"
    assert weather_data["description"] in [
        "clear sky", "few clouds", "overcast clouds",
        "smoke", "broken clouds", "scattered clouds", "rain"
    ], "Invalid weather description"

def test_generate_history_creates_records(db_session: Session, mocker):
    """
    Test that `generate_history` creates the correct number of records.
    """
    # Mock current time
    fixed_now = datetime(2024, 3, 3, 0, 0, 0)
    mocker.patch("app.data.get_current_time", return_value=fixed_now)
    
    days = 3
    generate_history(db=db_session, city="test_city", days=days, user_id=1)
    
    # Verify records
    records = db_session.query(WeatherRecord).filter_by(city="test_city", user_id=1).all()
    assert len(records) == days, f"Expected {days} records"










