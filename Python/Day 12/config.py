import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "654#sumu")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "shri#654")
    
    # Access token expires in 15 mins 
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    
    # Refresh token expires in 30 days
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    