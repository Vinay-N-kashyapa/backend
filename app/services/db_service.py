import logging
from supabase import create_client, Client
from app.config import settings

logger = logging.getLogger("pinit.db")

class DBService:
    _client: Client = None

    @classmethod
    def get_client(cls) -> Client:
        if cls._client is None:
            if not settings.supabase_url or not (settings.supabase_service_key or settings.supabase_key):
                logger.error("Supabase environment configuration variables are missing.")
                raise ValueError("Supabase environment configuration variables are missing.")
            
            # Prefer Service Role key on the backend to bypass RLS policies safely
            active_key = settings.supabase_service_key or settings.supabase_key
            try:
                cls._client = create_client(settings.supabase_url, active_key)
                logger.info("Supabase client initialized successfully on backend.")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                raise e
        return cls._client
