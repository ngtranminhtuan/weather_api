import pytest
from app.services.weather_service import get_current_weather
from app.models.weather import WeatherResponse

@pytest.mark.asyncio
async def test_get_current_weather(monkeypatch):
    async def mock_get_current_weather(location):
        return WeatherResponse(location=location, temperature=25.0)
    
    monkeypatch.setattr('app.services.weather_service.get_current_weather', mock_get_current_weather)    
    response = await get_current_weather("Osaka,jp")
    
    assert response.location == "Osaka,jp"
    assert type(response.temperature) == float
