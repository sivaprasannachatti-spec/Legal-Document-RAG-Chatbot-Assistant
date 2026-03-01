import os

from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
SUPABASE_PROJECT_URL = os.environ.get("SUPABASE_PROJECT_URL")

supabase = create_client(SUPABASE_PROJECT_URL, SUPABASE_API_KEY)
