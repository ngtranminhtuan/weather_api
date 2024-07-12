import aiohttp
from app.core.config import settings
from app.models.weather import WeatherResponse

async def get_current_weather(location: str) -> WeatherResponse:
    url = f"{settings.weather_api_url}?q={location}&appid={settings.weather_api_key}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    
    if response.status != 200:
        raise ValueError(data.get("message", "Failed to get weather data"))

    kelvin_temp = data['main']['temp']
    celsius_temp = kelvin_temp - 273.15
    return WeatherResponse(location=location, temperature=round(celsius_temp, 2))
