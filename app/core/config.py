 
# from pydantic_settings import BaseSettings
# from typing import Optional
# import os

# class Settings(BaseSettings):
#     DATABASE_URL: str = "sqlite:///./finance_assistant.db"
#     SECRET_KEY: str = "bcibsabcao873r619&^83he489dhjv1ui31dksbcbask"
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
#     vite_api_base_url: str
    
#     class Config:
#         env_file = ".env"

# settings = Settings()

from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./finance_assistant.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "asdfghjkl;")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000")

settings = Settings()