import requests
import json
from redis import Redis
from .config import settings

redis = Redis.from_url(settings.REDIS_URL)

def get_weather_data(city: str):
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "q": city,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric"
        }
    )
    response.raise_for_status()
    data = response.json()
    return {
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"]
    }








































































































































































