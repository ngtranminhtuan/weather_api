import aiohttp
from app.config.settings import settings
from app.models.weather import WeatherResponse
from app.services.openai_service import OpenAIService
from typing import List

class WeatherService:
    def __init__(self, settings, llm_service: OpenAIService):
        self.settings = settings
        self.llm_service = llm_service

    async def get_current_weather(self, location: str) -> WeatherResponse:
        url = f"{self.settings.weather_api_url}?q={location}&appid={self.settings.weather_api_key}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()

            if response.status != 200:
                raise ValueError(data.get("message", "Failed to get weather data"))

            kelvin_temp = data['main']['temp']
            celsius_temp = kelvin_temp - 273.15
            return WeatherResponse(location=location, temperature=round(celsius_temp, 2))
        
        except aiohttp.ClientError as e:
            raise ValueError(f"HTTP Client error: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Weather data error: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}")

    async def chat_weather(self, messages: List[dict]) -> str:
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

        try:
            response_data = await self.llm_service.get_weather_info(messages, tools)
            location = response_data['location']
            weather_data = await self.get_current_weather(location)
            human_readable_response = await self.llm_service.generate_human_readable_response(location, weather_data.model_dump())
            return human_readable_response
        
        except ValueError as e:
            raise ValueError(f"LLM or weather service error: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}")