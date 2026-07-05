"""
Application configuration.

Loads settings from environment variables / a .env file so secrets like the
MongoDB URI are never hard-coded in source control.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "predictive_maintenance"
    openai_api_key: str = ""
    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
