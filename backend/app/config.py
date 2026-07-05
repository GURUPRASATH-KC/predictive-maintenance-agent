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

    def get_cors_origins(self) -> list[str]:
        origins = {self.frontend_origin, "http://localhost:5173", "http://127.0.0.1:5173"}
        if self.frontend_origin and self.frontend_origin not in origins:
            origins.add(self.frontend_origin)
        return sorted(origins)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
