from sqlalchemy import Boolean, Column, Integer, String, Float, Time
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    content = Column(String(100))
    user_id = Column(Integer)

class Drone(Base):
    dronetype = Column(String(50))
    target_longitude = Column(Integer)
    target_latitude = Column(Float)
    radius_km = Column(Float)
    altitude_meters = Column(Integer)
    duration_minutes = Column(Time)