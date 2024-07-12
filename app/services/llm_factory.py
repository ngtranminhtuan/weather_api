from app.services.openai_service import OpenAIService
from app.config.settings import settings

class LLMFactory:
    @staticmethod
    def get_llm_service(llm_type: str):
        if llm_type == "openai":
            return OpenAIService(settings)
        # Add more LLMs here
        else:
            raise ValueError(f"Unsupported LLM type: {llm_type}")
