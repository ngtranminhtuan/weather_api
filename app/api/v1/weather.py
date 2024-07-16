from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.weather_service import WeatherService

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatWeatherRequest(BaseModel):
    messages: List[Message]

def weather_router(weather_service: WeatherService):
    @router.get("/weather")
    async def read_weather(location: str):
        try:
            return await weather_service.get_current_weather(location)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.post("/chat_weather")
    async def chat_weather(request: ChatWeatherRequest):
        try:
            messages = [message.dict() for message in request.messages]
            response = await weather_service.chat_weather(messages)
            return response
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    return router
