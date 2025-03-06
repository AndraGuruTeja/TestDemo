
# from datetime import datetime, timedelta
# from sqlalchemy.orm import Session
# from app.data import generate_history, get_current_time
# from app.models import WeatherRecord
# from unittest.mock import patch

# def test_generate_history_deletes_existing_records(db_session: Session, mocker):
#     """
#     Test that `generate_history` deletes existing records.
#     """
#     # Mock current time
#     fixed_now = datetime(2024, 3, 3, 0, 0, 0)
#     mocker.patch("app.data.get_current_time", return_value=fixed_now)
    
#     # Create test record within the date range
#     test_record = WeatherRecord(
#         city="test_city",
#         timestamp=fixed_now - timedelta(days=1),  # 2024-03-02 00:00:00
#         user_id=1
#     )
#     db_session.add(test_record)
#     db_session.commit()

#     # Generate history for the same city, user, and date range
#     generate_history(db=db_session, city="test_city", days=1, user_id=1)
    
#     # Verify deletion
#     deleted_record = db_session.query(WeatherRecord).filter_by(id=test_record.id).first()
#     assert deleted_record is None, "Record was not deleted"

# def test_generate_history_creates_correct_entries(db_session: Session, mocker):
#     """
#     Test that `generate_history` creates correct entries.
#     """
#     # Mock current time
#     fixed_now = datetime(2024, 3, 3, 0, 0, 0)
#     mocker.patch("app.data.get_current_time", return_value=fixed_now)
    
#     days = 2
#     generate_history(db=db_session, city="test_city", days=days, user_id=1)
    
#     # Verify records
#     records = db_session.query(WeatherRecord).filter_by(city="test_city", user_id=1).all()
#     assert len(records) == days, f"Expected {days} records"
    
#     # Verify timestamps
#     expected_dates = [
#         (fixed_now - timedelta(days=days) + timedelta(days=i)).replace(hour=12)
#         for i in range(days)
#     ]
#     for record, expected_date in zip(records, expected_dates):
#         assert record.timestamp == expected_date, f"Expected {expected_date}"




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