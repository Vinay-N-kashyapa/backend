import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    supabase_url: str = os.getenv("NEXT_PUBLIC_SUPABASE_URL", "")
    supabase_key: str = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY", "")
    supabase_service_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    port: int = int(os.getenv("PORT", "8000"))

    class Config:
        env_file = ".env"

settings = Settings()
