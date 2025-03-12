
# from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
# from sqlalchemy.orm import relationship
# from .database import Base
# from datetime import datetime

# class WeatherRecord(Base):
#     __tablename__ = "weather_records"
#     id = Column(Integer, primary_key=True, index=True)
#     city = Column(String)
#     temperature = Column(Float)
#     humidity = Column(Float)
#     description = Column(String)
#     timestamp = Column(DateTime, default=datetime.utcnow)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     owner = relationship("User", back_populates="weather_records")



# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     weather_records = relationship("WeatherRecord", back_populates="owner")




from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from .database import Base  # Ensure Base is correctly imported
from datetime import datetime

class WeatherRecord(Base):
    __tablename__ = "weather_records"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="weather_records")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    weather_records = relationship("WeatherRecord", back_populates="owner")
