import pytest
from unittest.mock import AsyncMock, patch
from app.services.weather_service import WeatherService
from app.config.settings import settings
from app.services.openai_service import OpenAIService

@pytest.fixture
def openai_service():
    return OpenAIService(settings)

@pytest.fixture
def weather_service(openai_service):
    return WeatherService(settings, openai_service)

@pytest.mark.asyncio
async def test_get_current_weather(weather_service):
    location = "Osaka,jp"
    weather_data = {
        "main": {
            "temp": 300.15
        }
    }
    mock_response = AsyncMock()
    mock_response.json = AsyncMock(return_value=weather_data)
    mock_response.status = 200

    with patch('aiohttp.ClientSession.get', new_callable=AsyncMock) as mock_get:
        mock_get.return_value.__aenter__.return_value = mock_response

        response = await weather_service.get_current_weather(location)
        assert response.location == location
        assert response.temperature == 27.0

@pytest.mark.asyncio
async def test_chat_weather(weather_service):
    messages = [{"role": "user", "content": "What's the weather in Osaka?"}]
    response_data = {"location": "Osaka,jp"}
    weather_data = {
        "main": {
            "temp": 300.15
        }
    }
    human_readable_response = "The weather in Osaka is 27.0°C"

    with patch.object(weather_service.llm_service, 'get_weather_info', new_callable=AsyncMock) as mock_get_weather_info, \
         patch.object(weather_service, 'get_current_weather', new_callable=AsyncMock) as mock_get_current_weather, \
         patch.object(weather_service.llm_service, 'generate_human_readable_response', new_callable=AsyncMock) as mock_generate_response:

        mock_get_weather_info.return_value = response_data
        mock_get_current_weather.return_value = AsyncMock(location="Osaka,jp", temperature=27.0)
        mock_generate_response.return_value = human_readable_response

        response = await weather_service.chat_weather(messages)
        assert response == human_readable_response
