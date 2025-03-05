import pytest
from datetime import datetime, timezone  # Updated import
from app.data import generate_fake_weather_data
from app.database import SessionLocal, Base
from app.models import WeatherRecord
from sqlalchemy import create_engine

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db_session():
    """Create a test database session"""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal(bind=engine)
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_generate_fake_weather_data():
    """Test the fake weather data generation function"""
    data = generate_fake_weather_data("London")
    assert isinstance(data, dict)
    assert "city" in data
    assert "temperature" in data
    assert "humidity" in data
    assert "description" in data
    assert 25 <= data["temperature"] <= 40
    assert 10 <= data["humidity"] <= 80

def test_database_operations(db_session):
    """Test database CRUD operations"""
    test_record = WeatherRecord(
        city="London",
        temperature=15.5,
        humidity=75,
        description="cloudy",
        timestamp=datetime.now(timezone.utc),  # Updated
        user_id=1
    )
    db_session.add(test_record)
    db_session.commit()
    
    result = db_session.query(WeatherRecord).filter_by(city="London").first()
    assert result is not None
    assert result.temperature == 15.5
    assert result.description == "cloudy"
    
    db_session.delete(result)
    db_session.commit()

def test_database_query_with_fake_data(db_session):
    """Test database operations with fake weather data"""
    fake_data = generate_fake_weather_data("Paris")
    record = WeatherRecord(
        city=fake_data["city"],
        temperature=fake_data["temperature"],
        humidity=fake_data["humidity"],
        description=fake_data["description"],
        timestamp=datetime.now(timezone.utc),  # Updated
        user_id=1
    )
    db_session.add(record)
    db_session.commit()
    
    result = db_session.query(WeatherRecord).filter_by(city="Paris").first()
    assert result is not None
    assert result.temperature == fake_data["temperature"]
    assert result.description == fake_data["description"]
    
    db_session.delete(result)
    db_session.commit()