import pytest
from unittest.mock import patch, MagicMock
from app.services.weather_service import WeatherService
from app.models.weather import WeatherResponse
from unittest.mock import AsyncMock, ANY
from app.services.openai_service import OpenAIService

@pytest.mark.asyncio
async def test_get_current_weather():
    # Set up mock data for the response
    mock_data = {
        'main': {'temp': 293.15},  # Kelvin temperature
        'message': 'Success'
    }

    # Set up a mock response object
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = mock_data

    # Patch the aiohttp.ClientSession class
    with patch('aiohttp.ClientSession') as mock_session:
        # Setup the context management correctly
        mock_instance = mock_session.return_value
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.get.return_value.__aenter__.return_value = mock_response
        mock_instance.get.return_value.__aexit__.return_value = None

        # Initialize the WeatherService with mock settings and llm_service
        settings = AsyncMock(weather_api_key='fake_key', weather_api_url='https://fakeurl.com')
        llm_service = AsyncMock(spec=OpenAIService)
        service = WeatherService(settings, llm_service)

        # Call the method
        result = await service.get_current_weather('Tokyo')
        assert isinstance(result, WeatherResponse)
        assert result.location == 'Tokyo'
        assert result.temperature == round(293.15 - 273.15, 2)  # Check conversion to Celsius

        # Ensure the 'get' method was correctly called
        mock_instance.get.assert_called_once_with('https://fakeurl.com?q=Tokyo&appid=fake_key')


@pytest.mark.asyncio
async def test_chat_weather():
    # Mock settings and OpenAIService
    settings = AsyncMock(weather_api_key='fake_key', weather_api_url='https://fakeurl.com')
    llm_service = AsyncMock(spec=OpenAIService)
    weather_service = WeatherService(settings, llm_service)

    # Setup mock for get_weather_info and generate_human_readable_response
    llm_service.get_weather_info.return_value = {
        'location': 'Tokyo',
        'temperature': 25,
        'description': 'sunny'
    }
    llm_service.generate_human_readable_response.return_value = "It is sunny in Tokyo with a temperature of 25°C."

    # Test input
    messages = [{'role': 'user', 'content': 'What is the weather in Tokyo today?'}]

    # Comprehensive patching to ensure all network calls are intercepted
    with patch('aiohttp.ClientSession') as mock_session:
        # Configure mock to handle context management and get method
        mock_instance = mock_session.return_value
        mock_instance.__aenter__.return_value = mock_instance
        mock_get = AsyncMock()
        mock_get.__aenter__.return_value = AsyncMock(status=200, json=AsyncMock(return_value={
            'main': {'temp': 298.15},  # 25°C in Kelvin
            'weather': [{'main': 'Clear', 'description': 'clear sky'}],
            'name': 'Tokyo'
        }))
        mock_get.__aexit__.return_value = None
        mock_instance.get.return_value = mock_get

        # Call the method
        result = await weather_service.chat_weather(messages)

        # Assertions
        assert result == "It is sunny in Tokyo with a temperature of 25°C."
        assert mock_instance.get.call_count == 1, "Ensure that a HTTP GET call is mocked."

    # Verify method calls
    llm_service.get_weather_info.assert_called_once()
    llm_service.generate_human_readable_response.assert_called_once()
