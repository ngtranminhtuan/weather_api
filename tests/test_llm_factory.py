import pytest
from app.services.llm_factory import LLMFactory
from app.services.openai_service import OpenAIService

def test_get_llm_service_openai():
    llm_service = LLMFactory.get_llm_service("openai")
    assert isinstance(llm_service, OpenAIService)

def test_get_llm_service_invalid():
    with pytest.raises(ValueError):
        LLMFactory.get_llm_service("invalid")
