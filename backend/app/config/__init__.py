"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # MongoDB Configuration
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "pothole_detection"
    
    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # File Upload Configuration
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 10
    
    # API Configuration
    API_V1_PREFIX: str = "/api"
    CORS_ORIGINS: List[str] = ["*"]
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # Testing Credentials
    TEST_AUTHORITY_EMAIL: str = "admin@city.gov"
    TEST_AUTHORITY_PASSWORD: str = "admin123"
    TEST_CITIZEN_EMAIL: str = "citizen@test.com"
    TEST_CITIZEN_PASSWORD: str = "password123"
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Allow extra environment variables
        case_sensitive = True


settings = Settings()
