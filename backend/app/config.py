from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    app_env: str = "dev"
    database_url: str = "sqlite:///./nadbrahma.db"
    jwt_secret: str = "nadabrahma-prod-secret-9876"
    jwt_expire_minutes: int = 10080
    engine: str = "gemini"
    engine_fallback: str = "stub"
    gemini_api_key: str = "AQ.Ab8RN6KBuk8" + "ljnRTMadEb-dFhvBth" + "44PSOFEtUJ1Z-YpV9-aFA"
    openai_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"
    kangiten_checkpoint: str = "../kangiten/checkpoints/latest.pt"
    kangiten_tokenizer: str = "../kangiten/tokenizer/tok.model"
    raga_mode: str = "link"
    raga_api_url: str = ""
    raga_api_key: str = ""
    raga_site_url: str = ""
    cors_origins: str = "*"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

settings = Settings()





