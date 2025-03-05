
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List
from redis import asyncio as aioredis
import requests
from sqlalchemy import func, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import random
import json
from dotenv import load_dotenv
from .data import generate_history
from .models import WeatherRecord, User
import os
from sqlalchemy.orm import declarative_base



app = FastAPI()
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    REDIS_URL: str = os.getenv("REDIS_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY")

settings = Settings()
# Database setup
Base = declarative_base()




engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Security setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Redis setup
redis = aioredis.from_url(settings.REDIS_URL)

# FastAPI app
app = FastAPI()

# Rate limiting setup
@app.on_event("startup")
async def startup():
    await FastAPILimiter.init(redis)

# Helper functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_fake_weather_data(city: str):
    return {
        "temperature": round(random.uniform(10, 35), 2),
        "humidity": random.randint(30, 90),
        "description": random.choice([
            "clear sky", "few clouds", "scattered clouds",
            "broken clouds", "overcast clouds", "rain"
        ])
    }

# Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: str
    password: str

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    humidity: float
    description: str
    cached: bool = False

class HistoricalWeatherResponse(WeatherResponse):
    timestamp: datetime

class WeatherTrendResponse(BaseModel):
    date: str
    avg_temperature: float
    max_temperature: float
    min_temperature: float
    avg_humidity: float

# Authentication endpoints
@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = jwt.encode(
        {"sub": user.email, "user_id": user.id, "exp": datetime.utcnow() + timedelta(minutes=30)},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

# Weather endpoints
@app.get("/weather/{city}", response_model=WeatherResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_weather(
    city: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check Redis cache first
    cached = await redis.get(f"weather:{city}:{current_user.id}")
    if cached:
        return {**json.loads(cached), "cached": True}
    
    try:
        # Get real-time data
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
        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }
    except:
        # Fallback to fake data
        weather_data = generate_history(city)
        # weather_data["city"] = city
    
    # Store in database and cache
    db_record = WeatherRecord(
        **weather_data,
        user_id=current_user.id,
        timestamp=datetime.utcnow()
    )
    db.add(db_record)
    db.commit()
    
    await redis.setex(
        f"weather:{city}:{current_user.id}", 
        600,
        json.dumps(weather_data)
    )
    
    return {**weather_data, "cached": False}


@app.get("/weather/history/{city}", response_model=List[HistoricalWeatherResponse], dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_history(
    city: str,
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check Redis cache first
    cache_key = f"weather:history:{city}:{current_user.id}:{days}"
    cached = await redis.get(cache_key)
    if cached:
        # Return cached data with "cached": True
        return [{"cached": True, **item} for item in json.loads(cached)]
    
    # Generate fake historical data
    start_date = datetime.utcnow() - timedelta(days=days)    
    generate_history(city=city, days=days, user_id=current_user.id)
    
    # Fetch historical data from the database
    history_records = (
        db.query(WeatherRecord)
        .filter(
            WeatherRecord.city == city,
            WeatherRecord.user_id == current_user.id,
            WeatherRecord.timestamp >= start_date,
        )
        .order_by(WeatherRecord.timestamp.asc())
        .all()
    )

    # Convert ORM objects to dictionaries and serialize datetime
    history = [
        {
            "city": record.city,
            "temperature": record.temperature,
            "humidity": record.humidity,
            "description": record.description,
            "timestamp": record.timestamp.isoformat()  # Convert datetime to string
        }
        for record in history_records
    ]

    # Cache the result for 10 minutes
    await redis.setex(
        cache_key,
        600,  # 10 minutes
        json.dumps(history)
    )
    
    # Return fresh data with "cached": False
    return [{"cached": False, **item} for item in history]
@app.get("/weather/trends/{city}", response_model=List[WeatherTrendResponse], dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_trends(
    city: str,
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check Redis cache first
    cache_key = f"weather:trends:{city}:{current_user.id}:{days}"
    cached = await redis.get(cache_key)
    if cached:
        # Return cached data with "cached": True
        return [{"cached": True, **item} for item in json.loads(cached)]
    
    # Generate historical data if it doesn't exist
    generate_history(city=city, days=days, user_id=current_user.id)
    
    # Calculate the start date
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Fetch trends from the database
    trends = db.query(
        func.strftime("%Y-%m-%d", WeatherRecord.timestamp).label("date"),
        func.avg(WeatherRecord.temperature).label("avg_temp"),
        func.max(WeatherRecord.temperature).label("max_temp"),
        func.min(WeatherRecord.temperature).label("min_temp"),
        func.avg(WeatherRecord.humidity).label("avg_humidity")
    ).filter(
        WeatherRecord.city == city,
        WeatherRecord.user_id == current_user.id,
        WeatherRecord.timestamp >= start_date
    ).group_by("date").all()
    
    if not trends:
        raise HTTPException(status_code=404, detail="No trend data available")
    
    # Format the trends
    trends_response = [{
        "date": trend.date,
        "avg_temperature": round(trend.avg_temp, 1),
        "max_temperature": round(trend.max_temp, 1),
        "min_temperature": round(trend.min_temp, 1),
        "avg_humidity": round(trend.avg_humidity, 1)
    } for trend in trends]
    
    # Cache the result for 10 minutes
    await redis.setex(
        cache_key,
        600,  # 10 minutes
        json.dumps(trends_response)
    )
    
    # Return fresh data with "cached": False
    return [{"cached": False, **item} for item in trends_response]