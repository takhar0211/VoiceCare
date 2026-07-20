import asyncio
from backend.db.supabase_client import get_supabase
from dotenv import load_dotenv

load_dotenv("backend/.env")

db = get_supabase()

try:
    res = db.table("users").select("*").limit(1).execute()
    print("Users table exists. Data:", res.data)
except Exception as e:
    print("Error querying users:", e)

