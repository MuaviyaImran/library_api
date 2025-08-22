import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    APP_NAME = os.getenv("APP_NAME", "Library Management API")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DEBUG = os.getenv("DEBUG", "true") == "true"

    # API Configuration
    API_PORT = os.getenv("API_PORT", 8000)
