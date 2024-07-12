import aiohttp
from app.models.weather import WeatherResponse
from app.services.openai_service import OpenAIService
from app.config.settings import Settings

class WeatherService:
    def __init__(self, settings: Settings, llm_service: OpenAIService):
        self.settings = settings
        self.llm_service = llm_service

    async def get_current_weather(self, location: str) -> WeatherResponse:
        url = f"{self.settings.weather_api_url}?q={location}&appid={self.settings.weather_api_key}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy="http://proxy.mei.co.jp:8080") as response:
                data = await response.json()
        
        if response.status != 200:
            raise ValueError(data.get("message", "Failed to get weather data"))

        kelvin_temp = data['main']['temp']
        celsius_temp = kelvin_temp - 273.15
        return WeatherResponse(location=location, temperature=round(celsius_temp, 2))

    async def get_weather_info(self, messages, tools):
        return await self.llm_service.get_weather_info(messages, tools)

    async def generate_human_readable_response(self, location, weather_data):
        return await self.llm_service.generate_human_readable_response(location, weather_data)
