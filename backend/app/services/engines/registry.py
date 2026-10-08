import os
from app.config import settings
from app.services.engines.base import ConversationEngine
from app.services.engines.stub import StubEngine
from app.services.engines.gemini import GeminiEngine
from app.services.engines.openai_engine import OpenAIEngine

def get_engine(name: str) -> ConversationEngine:
    if name == "openai":
        return OpenAIEngine()
    if name == "gemini":
        return GeminiEngine()
    return StubEngine()

def get_primary_engine() -> ConversationEngine:
    return get_engine(settings.engine)

def get_fallback_engine() -> ConversationEngine:
    return get_engine(settings.engine_fallback)

