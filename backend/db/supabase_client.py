import os
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")

_client: Client | None = None


def get_supabase() -> Client:
    """Get singleton Supabase client instance.
    
    Configured for Vercel serverless: uses /tmp for any file storage
    since Vercel's filesystem is read-only except /tmp.
    """
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env"
            )
        
        # Use options that work in serverless environments
        options = ClientOptions(
            postgrest_client_timeout=10,
            storage_client_timeout=10,
            flow_type="implicit",
        )
        _client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY, options)
    return _client

