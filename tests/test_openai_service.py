import pytest
from unittest.mock import AsyncMock, patch
from app.services.openai_service import OpenAIService
from app.config.settings import settings

@pytest.fixture
def openai_service():
    return OpenAIService(settings)

@pytest.mark.asyncio
async def test_get_weather_info(openai_service):
    messages = [{"role": "user", "content": "What's the weather in Osaka?"}]
    tools = [
        {
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
        }
    ]
    with patch.object(openai_service.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
        mock_create.return_value = AsyncMock()
        mock_create.return_value.choices = [AsyncMock()]
        mock_create.return_value.choices[0].message = AsyncMock()
        mock_create.return_value.choices[0].message.tool_calls = [AsyncMock()]
        mock_create.return_value.choices[0].message.tool_calls[0].function = AsyncMock()
        mock_create.return_value.choices[0].message.tool_calls[0].function.arguments = '{"location": "Osaka,jp"}'

        response_data = await openai_service.get_weather_info(messages, tools)
        assert response_data['location'] == "Osaka,jp"

@pytest.mark.asyncio
async def test_generate_human_readable_response(openai_service):
    weather_data = {"temperature": 20}
    with patch.object(openai_service.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
        mock_create.return_value = AsyncMock()
        mock_create.return_value.choices = [AsyncMock()]
        mock_create.return_value.choices[0].message = AsyncMock()
        mock_create.return_value.choices[0].message.content = "The weather in Osaka is 20°C"

        response = await openai_service.generate_human_readable_response("Osaka", weather_data)
        assert response == "The weather in Osaka is 20°C"
