import pytest
import aiohttp
from unittest.mock import AsyncMock, patch
from app.services.weather_service import WeatherService
from app.services.openai_service import OpenAIService
from app.models.weather import WeatherResponse
from app.config.settings import Settings

@pytest.fixture
def settings():
    return Settings(
        openai_api_key="test_openai_api_key",
        weather_api_key="test_weather_api_key",
        weather_api_url="http://api.openweathermap.org/data/2.5/weather"
    )

@pytest.fixture
def openai_service(settings):
    return OpenAIService(settings)

@pytest.fixture
def weather_service(settings, openai_service):
    return WeatherService(settings, openai_service)

@pytest.mark.asyncio
async def test_get_current_weather(weather_service, settings):
    location = "Osaka,jp"
    mock_response_data = {
        "main": {
            "temp": 300.15
        }
    }
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_response_data)
        mock_get.return_value.__aenter__.return_value.status = 200
        
        response = await weather_service.get_current_weather(location)
        assert response.location == location
        assert response.temperature == 27.0

@pytest.mark.asyncio
async def test_get_current_weather_http_error(weather_service):
    location = "InvalidCity"
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value={"message": "city not found"})
        mock_get.return_value.__aenter__.return_value.status = 404
        
        with pytest.raises(ValueError) as excinfo:
            await weather_service.get_current_weather(location)
        assert "Weather data error: city not found" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_current_weather_client_error(weather_service):
    location = "Osaka,jp"
    with patch("aiohttp.ClientSession.get", side_effect=aiohttp.ClientError("Client Error")):
        with pytest.raises(ValueError) as excinfo:
            await weather_service.get_current_weather(location)
        assert "HTTP Client error" in str(excinfo.value)

@pytest.mark.asyncio
async def test_chat_weather(weather_service):
    messages = [{"role": "user", "content": "What's the weather in Osaka?"}]
    location = "Osaka,jp"
    weather_data = WeatherResponse(location=location, temperature=27.0)
    
    with patch.object(weather_service.llm_service, 'get_weather_info', return_value={"location": location}) as mock_get_weather_info:
        with patch.object(weather_service, 'get_current_weather', return_value=weather_data) as mock_get_current_weather:
            with patch.object(weather_service.llm_service, 'generate_human_readable_response', return_value="The current temperature in Osaka is 27.0°C.") as mock_generate_human_readable_response:
                
                response = await weather_service.chat_weather(messages)
                assert response == "The current temperature in Osaka is 27.0°C."
                mock_get_weather_info.assert_called_once_with(messages, [{
                    "type": "function",
                    "function": {
                        "name": "get_current_weather",
                        "description": "Get the current weather in a given location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and country, e.g. Osaka,jp",
                                },
                            },
                            "required": ["location"],
                        }
                    }
                }])
                mock_get_current_weather.assert_called_once_with(location)
                mock_generate_human_readable_response.assert_called_once_with(location, weather_data.model_dump())

@pytest.mark.asyncio
async def test_chat_weather_llm_error(weather_service):
    messages = [{"role": "user", "content": "What's the weather in Osaka?"}]
    
    with patch.object(weather_service.llm_service, 'get_weather_info', side_effect=ValueError("LLM Error")):
        with pytest.raises(ValueError) as excinfo:
            await weather_service.chat_weather(messages)
        assert "LLM or weather service error: LLM Error" in str(excinfo.value)
