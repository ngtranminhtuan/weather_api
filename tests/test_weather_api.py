import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from app.api.v1.weather import weather_router
from app.services.weather_service import WeatherService

# Mock WeatherService for testing
class MockWeatherService:
    async def get_current_weather(self, location: str):
        if location == "invalid":
            raise ValueError("Invalid location")
        return {"location": location, "temperature": 20.0}
    
    async def chat_weather(self, messages):
        if not messages:
            raise ValueError("Invalid request")
        return "The weather is sunny"

@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()
    mock_weather_service = MockWeatherService()
    app.include_router(weather_router(mock_weather_service), prefix="/api/v1")

    # Adding healthcheck endpoint to the app
    @app.get("/healthcheck")
    def read_healthcheck():
        return {"status": "ok"}

    return app

@pytest.fixture
def client(app: FastAPI):
    return TestClient(app)

@pytest.fixture
async def async_client(app: FastAPI):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

def test_healthcheck(client: TestClient):
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_read_weather(client: TestClient):
    response = client.get("/api/v1/weather?location=Tokyo")
    assert response.status_code == 200
    assert response.json() == {"location": "Tokyo", "temperature": 20.0}

def test_read_weather_invalid_location(client: TestClient):
    response = client.get("/api/v1/weather?location=invalid")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid location"}

@pytest.mark.asyncio
async def test_chat_weather(async_client):
    response = await async_client.post("/api/v1/chat_weather", json={
        "messages": [
            {"role": "user", "content": "What's the weather like?"}
        ]
    })
    assert response.status_code == 200
    assert response.json() == "The weather is sunny"

@pytest.mark.asyncio
async def test_chat_weather_invalid(async_client):
    response = await async_client.post("/api/v1/chat_weather", json={
        "messages": []
    })
    assert response.status_code == 400
    assert "Invalid request" in response.json()["detail"]
