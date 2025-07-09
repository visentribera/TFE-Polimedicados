# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str

    class Config:
        env_file = ".env"  # Indicamos que lea las variables de este archivo

settings = Settings()