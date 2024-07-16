from fastapi import FastAPI
from app.api.v1.weather import weather_router
from app.services.llm_factory import LLMFactory
from app.config.settings import settings
from app.services.weather_service import WeatherService

app = FastAPI()

# Create LLM Service
llm_service = LLMFactory.get_llm_service("openai")
weather_service = WeatherService(settings, llm_service)

app.include_router(weather_router(weather_service), prefix="/api/v1")

# Thêm endpoint healthcheck
@app.get("/healthcheck")
def read_healthcheck():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
