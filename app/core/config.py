from pydantic import BaseModel
import yaml
from typing import Any, Dict

class Settings(BaseModel):
    openai_api_key: str
    weather_api_key: str
    weather_api_url: str

def load_settings() -> Settings:
    with open("app/core/settings.yaml", "r") as f:
        config: Dict[str, Any] = yaml.safe_load(f)
    return Settings(**config)

settings: Settings = load_settings()
