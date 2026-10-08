from google import genai
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str = ""
    class Config:
        env_file = ".env"

settings = Settings()
client = genai.Client(api_key=settings.gemini_api_key)
print(dir(client.models))
