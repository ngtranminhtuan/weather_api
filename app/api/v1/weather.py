from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.models.weather import WeatherResponse
from app.services.weather_service import WeatherService

def router(weather_service: WeatherService):
    api_router = APIRouter()

    @api_router.get("/weather", response_model=WeatherResponse)
    async def read_weather(location: str) -> WeatherResponse:
        try:
            return await weather_service.get_current_weather(location)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    class Message(BaseModel):
        role: str
        content: str

    class ChatWeatherRequest(BaseModel):
        messages: List[Message]

    @api_router.post("/chat_weather", response_model=str)
    async def chat_weather(request: ChatWeatherRequest) -> str:
        messages = [message.model_dump() for message in request.messages]
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
        
        response_data = await weather_service.get_weather_info(messages, tools)
        location = response_data['location']
        weather_data = await weather_service.get_current_weather(location)
        
        human_readable_response = await weather_service.generate_human_readable_response(location, weather_data.model_dump())
        return human_readable_response

    return api_router
