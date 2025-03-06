
# from datetime import datetime, timedelta
# import random
# from .database import SessionLocal
# from .models import WeatherRecord

# def generate_fake_weather_data(city: str) -> dict:
#     """Generate single fake weather entry"""
#     return {
#         "city": city,
#         "temperature": round(random.uniform(25, 40), 2),
#         "humidity": random.randint(10, 80),
#         "description": random.choice([
#             "clear sky", "few clouds", "overcast clouds", 
#             "smoke", "broken clouds", "scattered clouds", "rain"
#         ])
#     }

# # def generate_history(city: str, days: int, user_id: int):
# #     """Generate historical data using the fake weather generator"""
# #     db = SessionLocal()
# #     try:
# #         end_date = datetime.utcnow()
# #         start_date = end_date - timedelta(days=days)

# #         existing_dates = {rec.timestamp.date() for rec in 
# #             db.query(WeatherRecord).filter(
# #                 WeatherRecord.city == city,
# #                 WeatherRecord.timestamp >= start_date,
# #                 WeatherRecord.user_id == user_id
# #             ).all()
# #         }

# #         current_date = start_date
# #         while current_date <= end_date:
# #             if current_date.date() not in existing_dates:
# #                 weather_data = generate_fake_weather_data(city)
# #                 weather_data.update({
# #                     "timestamp": current_date.replace(
# #                         hour=12, minute=0, second=0, microsecond=0
# #                     ),
# #                     "user_id": user_id
# #                 })
                
# #                 db.add(WeatherRecord(**weather_data))
# #             current_date += timedelta(days=1)
        
# #         db.commit()
# #     finally:
# #         db.close()






# def generate_history(city: str, days: int, user_id: int):
#     """Generate historical data using the fake weather generator"""
#     db = SessionLocal()
#     try:
#         end_date = datetime.utcnow()
#         start_date = end_date - timedelta(days=days)

#         # Delete existing records in the date range for this user and city
#         db.query(WeatherRecord).filter(
#             WeatherRecord.city == city,
#             WeatherRecord.timestamp >= start_date,
#             WeatherRecord.timestamp <= end_date,
#             WeatherRecord.user_id == user_id
#         ).delete()
#         db.commit()

#         current_date = start_date
#         while current_date <= end_date:
#             for hour in [0, 3, 6, 9, 12, 15, 18, 21]:
#                 timestamp = current_date.replace(hour=hour, minute=0, second=0, microsecond=0)
#                 weather_data = generate_fake_weather_data(city)
#                 weather_data.update({
#                     "timestamp": timestamp,
#                     "user_id": user_id
#                 })
#                 db.add(WeatherRecord(**weather_data))
#             current_date += timedelta(days=1)
        
#         db.commit()
#     finally:
#         db.close()







# from datetime import datetime, timedelta
# import random
# from sqlalchemy.orm import Session
# from .database import SessionLocal
# from .models import WeatherRecord

# def generate_fake_weather_data(city: str) -> dict:
#     """Generate realistic weather data for testing and fallback scenarios
    
#     Args:
#         city: City name for weather data generation
        
#     Returns:
#         dict: Generated weather data with keys:
#             - city (str)
#             - temperature (float)
#             - humidity (int)
#             - description (str)
#     """
#     return {
#         "city": city,
#         "temperature": round(random.uniform(25, 40), 2),
#         "humidity": random.randint(10, 80),
#         "description": random.choice([
#             "clear sky", "few clouds", "overcast clouds",
#             "smoke", "broken clouds", "scattered clouds", "rain"
#         ])
#     }

# def generate_history(db: Session, city: str, days: int, user_id: int) -> None:
#     """Generate and store historical weather data
    
#     Args:
#         db: Database session (dependency injection)
#         city: City to generate history for
#         days: Number of days of history to generate
#         user_id: Associated user ID
        
#     Workflow:
#         1. Delete existing records for the user/city/date-range
#         2. Generate 8 entries per day at 3-hour intervals
#         3. Commit all changes in a single transaction
#     """
#     try:
#         # Calculate date range
#         end_date = datetime.utcnow()
#         start_date = end_date - timedelta(days=days)

#         # Clear existing data
#         db.query(WeatherRecord).filter(
#             WeatherRecord.city == city,
#             WeatherRecord.timestamp >= start_date,
#             WeatherRecord.timestamp <= end_date,
#             WeatherRecord.user_id == user_id
#         ).delete()

#         # Generate new records
#         records = []
#         current_date = start_date
        
#         while current_date <= end_date:
#             for hour in [0, 3, 6, 9, 12, 15, 18, 21]:
#                 timestamp = current_date.replace(
#                     hour=hour, minute=0, second=0, microsecond=0
#                 )
#                 weather_data = generate_fake_weather_data(city)
#                 records.append(WeatherRecord(
#                     **weather_data,
#                     timestamp=timestamp,
#                     user_id=user_id
#                 ))
#             current_date += timedelta(days=1)

#         # Bulk insert for better performance
#         db.bulk_save_objects(records)
#         db.commit()
        
#     except Exception as e:
#         db.rollback()
#         raise


# from datetime import datetime, timedelta
# import random
# from sqlalchemy.orm import Session
# from app.models import WeatherRecord
# from typing import List, Dict

# def get_current_time() -> datetime:
#     """
#     Utility function to get the current time in UTC.
#     This function is designed to be easily mocked for testing.
#     """
#     return datetime.utcnow()

# def generate_fake_weather_data(city: str) -> Dict[str, any]:
#     """
#     Generate realistic fake weather data for testing and fallback scenarios.

#     Args:
#         city (str): The city for which weather data is generated.

#     Returns:
#         dict: A dictionary containing fake weather data.
#     """
#     return {
#         "city": city,
#         "temperature": round(random.uniform(25, 40)),  # Temperature in Celsius
#         "humidity": random.randint(10, 80),  # Humidity in percentage
#         "description": random.choice([
#             "clear sky", "few clouds", "overcast clouds",
#             "smoke", "broken clouds", "scattered clouds", "rain"
#         ])
#     }
# def generate_history(db: Session, city: str, days: int, user_id: int) -> None:
#     """
#     Generate and store historical weather data for a given city and user.

#     Args:
#         db (Session): SQLAlchemy database session.
#         city (str): The city for which historical data is generated.
#         days (int): The number of days of historical data to generate.
#         user_id (int): The ID of the user associated with the data.

#     Raises:
#         Exception: If an error occurs during the database operation.
#     """
#     try:
#         # Calculate date range based on midnight
#         end_date = get_current_time().replace(hour=0, minute=0, second=0, microsecond=0)
#         start_date = end_date - timedelta(days=days)

#         # Clear existing data within the date range
#         db.query(WeatherRecord).filter(
#             WeatherRecord.city == city,
#             WeatherRecord.user_id == user_id,
#             WeatherRecord.timestamp >= start_date,
#             WeatherRecord.timestamp <=end_date  # Use < to exclude end_date
#         ).delete(synchronize_session="fetch")  # Force deletion
#         db.commit()  # Commit the deletion

#         # Generate new records (one entry per day)
#         records: List[WeatherRecord] = []
#         current_date = start_date

#         for _ in range(days):
#             # Set timestamp to midday (12:00 PM) for consistency
#             timestamp = current_date.replace(hour=12, minute=0, second=0, microsecond=0)
#             weather_data = generate_fake_weather_data(city)
#             records.append(WeatherRecord(
#                 **weather_data,
#                 timestamp=timestamp,
#                 user_id=user_id
#             ))
#             current_date += timedelta(days=1)

#         # Bulk insert the generated records
#         db.bulk_save_objects(records)
#         db.commit()
#     except Exception as e:
#         # Rollback the transaction in case of an error
#         db.rollback()
#         raise RuntimeError(f"Failed to generate historical data: {e}")










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