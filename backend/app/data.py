
from datetime import datetime, timedelta
import random
from .database import SessionLocal
from .models import WeatherRecord

def generate_fake_weather_data(city: str) -> dict:
    """Generate single fake weather entry"""
    return {
        "city": city,
        "temperature": round(random.uniform(25, 40), 2),
        "humidity": random.randint(10, 80),
        "description": random.choice([
            "clear sky", "few clouds", "overcast clouds", 
            "smoke", "broken clouds", "scattered clouds", "rain"
        ])
    }

# def generate_history(city: str, days: int, user_id: int):
#     """Generate historical data using the fake weather generator"""
#     db = SessionLocal()
#     try:
#         end_date = datetime.utcnow()
#         start_date = end_date - timedelta(days=days)

#         existing_dates = {rec.timestamp.date() for rec in 
#             db.query(WeatherRecord).filter(
#                 WeatherRecord.city == city,
#                 WeatherRecord.timestamp >= start_date,
#                 WeatherRecord.user_id == user_id
#             ).all()
#         }

#         current_date = start_date
#         while current_date <= end_date:
#             if current_date.date() not in existing_dates:
#                 weather_data = generate_fake_weather_data(city)
#                 weather_data.update({
#                     "timestamp": current_date.replace(
#                         hour=12, minute=0, second=0, microsecond=0
#                     ),
#                     "user_id": user_id
#                 })
                
#                 db.add(WeatherRecord(**weather_data))
#             current_date += timedelta(days=1)
        
#         db.commit()
#     finally:
#         db.close()






def generate_history(city: str, days: int, user_id: int):
    """Generate historical data using the fake weather generator"""
    db = SessionLocal()
    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        # Delete existing records in the date range for this user and city
        db.query(WeatherRecord).filter(
            WeatherRecord.city == city,
            WeatherRecord.timestamp >= start_date,
            WeatherRecord.timestamp <= end_date,
            WeatherRecord.user_id == user_id
        ).delete()
        db.commit()

        current_date = start_date
        while current_date <= end_date:
            for hour in [0, 3, 6, 9, 12, 15, 18, 21]:
                timestamp = current_date.replace(hour=hour, minute=0, second=0, microsecond=0)
                weather_data = generate_fake_weather_data(city)
                weather_data.update({
                    "timestamp": timestamp,
                    "user_id": user_id
                })
                db.add(WeatherRecord(**weather_data))
            current_date += timedelta(days=1)
        
        db.commit()
    finally:
        db.close()