import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Security
SECRET_KEY = os.getenv('SECRET_KEY')

# Flask configuration
DEBUG = True  # Set to False in production 