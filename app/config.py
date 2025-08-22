"""Application configuration using environment variables via pydantic-settings."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	# API metadata
	project_name: str = "Auth API"

	# Security configuration for JWT
	secret_key: str = "CHANGE_ME"  # override via env: SECRET_KEY
	algorithm: str = "HS256"
	access_token_expire_minutes: int = 60

	# Database connection URL (defaults to local sqlite file)
	database_url: str = "sqlite:///./app.db"

	class Config:
		# Load variables from .env if present
		env_file = ".env"


settings = Settings()
