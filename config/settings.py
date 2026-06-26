import os
from functools import lru_cache
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    """
    Application settings validated with Pydantic.
    Holds configuration details for the CareerForge Engine and Streamlit UI.
    """
    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    gemini_api_key: str | None = Field(default=None, alias="GEMINI_API_KEY")
    database_url: str = Field(default="sqlite:///./aeterna.db", alias="DATABASE_URL")
    secret_key: str = Field(default="dev_secret_key_placeholder_change_me", alias="SECRET_KEY")

    model_config = {
        "populate_by_name": True,
        "frozen": True,
    }

    @property
    def is_development(self) -> bool:
        return self.app_env.lower() == "development"

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached, validated singleton instance of Settings.
    Reads from os.environ after loading .env.
    """
    # Instantiate using env variables
    return Settings(
        APP_ENV=os.getenv("APP_ENV", "development"),
        LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO"),
        GEMINI_API_KEY=os.getenv("GEMINI_API_KEY"),
        DATABASE_URL=os.getenv("DATABASE_URL", "sqlite:///./aeterna.db"),
        SECRET_KEY=os.getenv("SECRET_KEY", "dev_secret_key_placeholder_change_me")
    )
