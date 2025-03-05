# import requests
# from .config import Config
# from .cache import get_cached_weather, cache_weather

# def fetch_weather_data(city: str):
#     url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={Config.API_KEY}&units=metric"
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.json()

# def get_weather_service(city: str):
#     if cached := get_cached_weather(city):
#         return eval(cached)
    
#     data = fetch_weather_data(city)
#     weather_data = {
#         "city": data["name"],
#         "temperature": data["main"]["temp"],
#         "humidity": data["main"]["humidity"],
#         "wind_speed": data["wind"]["speed"],
#         "description": data["weather"][0]["description"]
        
        
#     }
    
#     cache_weather(city, weather_data)
#     return weather_data













# import requests
# from .config import Config
# from .cache import get_cached_weather, cache_weather
# from fastapi import HTTPException

# def fetch_weather_data(city: str):
#     try:
#         url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={Config.API_KEY}&units=metric"
#         response = requests.get(url)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Weather API error: {str(e)}"
#         )

# def get_weather_service(city: str):
#     try:
#         if cached := get_cached_weather(city):
#             return eval(cached)
        
#         data = fetch_weather_data(city)
#         weather_data = {
#             "city": data["name"],
#             "temperature": data["main"]["temp"],
#             "humidity": data["main"]["humidity"],
#             "wind_speed": data["wind"]["speed"],
#             "description": data["weather"][0]["description"]
#         }
        
#         cache_weather(city, weather_data)
#         return weather_data
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Service error: {str(e)}"
#         )


































































































































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







































































































































































