from openai import OpenAI
import json
from typing import List, Dict, Any
from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)

async def get_weather_info(messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> Dict[str, Any]:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    arguments = response.choices[0].message.tool_calls[0].function.arguments
    data_json = json.loads(arguments)
    return data_json

async def generate_human_readable_response(location: str, weather_data: Dict[str, Any]) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Answer this weather information in celsius."},
        {"role": "user", "content": f"Here is the weather in {location}: {weather_data}"},
    ]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    return response.choices[0].message.content
