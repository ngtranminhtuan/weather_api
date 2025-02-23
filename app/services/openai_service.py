from openai import OpenAI, AsyncOpenAI
import json
from typing import List, Dict, Any
from app.config.settings import Settings
from fastapi import HTTPException

class OpenAIService:
    def __init__(self, settings: Settings):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def get_weather_info(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            # Check if the finish_reason is 'tool_calls'
            if response.choices and response.choices[0].finish_reason == 'tool_calls':
                arguments = response.choices[0].message.tool_calls[0].function.arguments
                data_json = json.loads(arguments)
                return data_json
            else:
                # If finish_reason is not 'tool_calls', return the assistant's message
                assistant_message = response.choices[0].message.content
                raise HTTPException(status_code=400, detail={"error": "No tool calls detected.", "message": assistant_message})
            
        except Exception as e:
            raise HTTPException(status_code=400, detail={"error": str(e)})

    async def generate_human_readable_response(self, location: str, weather_data: Dict[str, Any]) -> str:
        try:
            messages = [
                {"role": "system", "content": "You are a helpful assistant. Answer this weather information in celsius."},
                {"role": "user", "content": f"Here is the weather in {location}: {weather_data}"},
            ]
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise HTTPException(status_code=400, detail={"error": str(e)})
