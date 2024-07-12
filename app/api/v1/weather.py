from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.weather_service import get_current_weather
from app.tools.openai_tool import get_weather_info, generate_human_readable_response
from app.models.weather import WeatherResponse

router = APIRouter()

@router.get("/weather", response_model=WeatherResponse)
async def read_weather(location: str) -> WeatherResponse:
    try:
        return await get_current_weather(location)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

class Message(BaseModel):
    role: str
    content: str

class ChatWeatherRequest(BaseModel):
    messages: List[Message]

@router.post("/chat_weather", response_model=str)
async def chat_weather(request: ChatWeatherRequest) -> str:
    messages = [message.dict() for message in request.messages]
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
    
    response_data = await get_weather_info(messages, tools)
    location = response_data['location']
    weather_data = await get_current_weather(location)
    
    human_readable_response = await generate_human_readable_response(location, weather_data.dict())
    return human_readable_response
