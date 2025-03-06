
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from app.models import WeatherRecord
from typing import List, Dict

def get_current_time() -> datetime:
    """
    Utility function to get the current time in UTC.
    This function is designed to be easily mocked for testing.
    """
    return datetime.utcnow()

def generate_fake_weather_data(city: str) -> Dict[str, any]:
    """
    Generate realistic fake weather data for testing and fallback scenarios.

    Args:
        city (str): The city for which weather data is generated.

    Returns:
        dict: A dictionary containing fake weather data.
    """
    return {
        "city": city,
        "temperature": round(random.uniform(25, 40)),  # Temperature in Celsius
        "humidity": random.randint(10, 80),  # Humidity in percentage
        "description": random.choice([
            "clear sky", "few clouds", "overcast clouds",
            "smoke", "broken clouds", "scattered clouds", "rain"
        ])
    }

def generate_history(db: Session, city: str, days: int, user_id: int) -> None:
    """
    Generate and store historical weather data for a given city and user.

    Args:
        db (Session): SQLAlchemy database session.
        city (str): The city for which historical data is generated.
        days (int): The number of days of historical data to generate.
        user_id (int): The ID of the user associated with the data.

    Raises:
        Exception: If an error occurs during the database operation.
    """
    try:
        # Calculate date range based on midnight
        end_date = get_current_time().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = end_date - timedelta(days=days)

        # Clear existing data within the date range
        db.query(WeatherRecord).filter(
            WeatherRecord.city == city,
            WeatherRecord.user_id == user_id,
            WeatherRecord.timestamp >= start_date,
            WeatherRecord.timestamp <= end_date  # Use <= to include end_date
        ).delete(synchronize_session="fetch")  # Force deletion
        db.commit()  # Commit the deletion

        # Generate new records (one entry per day)
        records: List[WeatherRecord] = []
        current_date = start_date

        for _ in range(days):
            # Set timestamp to midday (12:00 PM) for consistency
            timestamp = current_date.replace(hour=12, minute=0, second=0, microsecond=0)
            weather_data = generate_fake_weather_data(city)
            records.append(WeatherRecord(
                **weather_data,
                timestamp=timestamp,
                user_id=user_id
            ))
            current_date += timedelta(days=1)

        # Bulk insert the generated records
        db.bulk_save_objects(records)
        db.commit()
    except Exception as e:
        # Rollback the transaction in case of an error
        db.rollback()
        raise RuntimeError(f"Failed to generate historical data: {e}")