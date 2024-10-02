import os
from datetime import timedelta

class Config:
    
    # Secret key for signing jwt and csrf tokens
    SECRET_KEY = os.environ.get('SECRET_KEY') or '654#sumu'
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///ecommerce.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'shri#654'
    
    # Access token expires in 15 mins 
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    
    # Refresh token expires in 30 days
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Enable jwt blacklisting
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    
    # Other optional configuration
    PROPAGATE_EXCEPTIONS = True
    

# Development config
class DevelopmentConfig(Config):
    DEBUG = True

# Production config
class ProductionConfig(Config):
    DEBUG = True
    
# Config selector based on environment variable
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
    