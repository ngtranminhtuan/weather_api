import pytest
from unittest.mock import patch, AsyncMock
from fastapi import HTTPException
from app.services.openai_service import OpenAIService
from app.config.settings import Settings

@pytest.mark.asyncio
async def test_get_weather_info_success():
    # Mock settings
    settings = Settings(openai_api_key='fake_openai_key', weather_api_key='fake_weather_key', weather_api_url='https://fakeurl.com')
    
    # Initialize the OpenAIService with mock settings
    service = OpenAIService(settings)

    # Mock response from OpenAI API
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].finish_reason = 'tool_calls'
    mock_response.choices[0].message = AsyncMock()
    mock_response.choices[0].message.tool_calls = [AsyncMock()]
    mock_response.choices[0].message.tool_calls[0].function = AsyncMock()
    mock_response.choices[0].message.tool_calls[0].function.arguments = '{"location": "Tokyo", "temperature": 25, "description": "sunny"}'
    
    # Patch the OpenAI client
    with patch.object(service.client.chat.completions, 'create', return_value=mock_response):
        messages = [{'role': 'user', 'content': 'What is the weather in Tokyo today?'}]
        tools = [{'type': 'function', 'function': {'name': 'get_current_weather', 'parameters': {}}}]
        
        result = await service.get_weather_info(messages, tools)

        assert result['location'] == 'Tokyo'
        assert result['temperature'] == 25
        assert result['description'] == 'sunny'

        # Verify that the OpenAI API was called with the expected arguments
        service.client.chat.completions.create.assert_called_once_with(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

@pytest.mark.asyncio
async def test_get_weather_info_failure():
    # Mock settings
    settings = Settings(openai_api_key='fake_openai_key', weather_api_key='fake_weather_key', weather_api_url='https://fakeurl.com')
    
    # Initialize the OpenAIService with mock settings
    service = OpenAIService(settings)

    # Mock response from OpenAI API for failure
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].finish_reason = 'stop'
    mock_response.choices[0].message = AsyncMock()
    mock_response.choices[0].message.content = "I'm an AI language model designed to assist with answering questions, providing information, and helping with various tasks through conversation. How can I help you today?"

    # Patch the OpenAI client
    with patch.object(service.client.chat.completions, 'create', return_value=mock_response):
        messages = [{'role': 'user', 'content': 'Tell me about AI models.'}]
        tools = [{'type': 'function', 'function': {'name': 'get_current_weather', 'parameters': {}}}]
        
        with pytest.raises(HTTPException) as exc_info:
            await service.get_weather_info(messages, tools)
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == {
            "error": "No tool calls detected.",
            "message": "I'm an AI language model designed to assist with answering questions, providing information, and helping with various tasks through conversation. How can I help you today?"
        }

@pytest.mark.asyncio
async def test_generate_human_readable_response():
    # Mock settings
    settings = Settings(openai_api_key='fake_openai_key', weather_api_key='fake_weather_key', weather_api_url='https://fakeurl.com')
    
    # Initialize the OpenAIService with mock settings
    service = OpenAIService(settings)

    # Mock response from OpenAI API
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message = AsyncMock()
    mock_response.choices[0].message.content = "It is sunny in Tokyo with a temperature of 25°C."

    # Patch the OpenAI client
    with patch.object(service.client.chat.completions, 'create', return_value=mock_response):
        location = 'Tokyo'
        weather_data = {'location': 'Tokyo', 'temperature': 25, 'description': 'sunny'}
        
        result = await service.generate_human_readable_response(location, weather_data)

        assert result == "It is sunny in Tokyo with a temperature of 25°C."

        # Verify that the OpenAI API was called with the expected arguments
        service.client.chat.completions.create.assert_called_once_with(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Answer this weather information in celsius."},
                {"role": "user", "content": f"Here is the weather in {location}: {weather_data}"},
            ]
        )
