import os
from datetime import timedelta

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///pointr.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    AUTH_TOKENS = os.environ.get('AUTH_TOKENS', 'test-token').split(',')
    
    # Application
    DEBUG = os.environ.get('FLASK_ENV') == 'development'