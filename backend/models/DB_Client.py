import os

from supabase import create_client

supabase = create_client(os.environ["SUPABASE_API_KEY"], os.environ["SUPABASE_PROJECT_URL"])
