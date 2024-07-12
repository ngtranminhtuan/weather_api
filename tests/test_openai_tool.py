import pytest
from app.tools.openai_tool import get_weather_info, generate_human_readable_response

@pytest.mark.asyncio
async def test_get_weather_info(monkeypatch):
    async def mock_get_weather_info(messages, tools):
        return {"location": "Osaka,jp"}
    
    monkeypatch.setattr('app.tools.openai_tool', 'get_weather_info', mock_get_weather_info)
    
    messages = [{"role": "user", "content": "What is the weather in Osaka,jp?"}]
    tools = [{
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
    }]
    
    response = await get_weather_info(messages, tools)
    assert response["location"] == "Osaka,jp"

@pytest.mark.asyncio
async def test_generate_human_readable_response(monkeypatch):
    async def mock_generate_human_readable_response(location, weather_data):
        return "The temperature in Osaka, Japan is 25.0°C."
    
    monkeypatch.setattr('app.tools.openai_tool', 'generate_human_readable_response', mock_generate_human_readable_response)
    
    location = "Osaka,jp"
    weather_data = {"location": location, "temperature": 25.0}
    
    response = await generate_human_readable_response(location, weather_data)
    assert response == "The temperature in Osaka, Japan is 25.0°C."
