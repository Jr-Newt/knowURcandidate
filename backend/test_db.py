"""Quick diagnostic script to test Supabase connection and identify errors."""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

print(f"URL: {SUPABASE_URL[:30]}...")
print(f"KEY: {SUPABASE_KEY[:20]}...")

from supabase import create_client
client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Test 1: Try to list districts
print("\n--- Test 1: List districts ---")
try:
    res = client.table("districts").select("*").execute()
    print(f"Success! Found {len(res.data)} districts")
    if res.data:
        for d in res.data[:3]:
            print(f"  {d}")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")

# Test 2: Try to list candidates
print("\n--- Test 2: List candidates ---")
try:
    res = client.table("candidates").select("*").limit(3).execute()
    print(f"Success! Found {len(res.data)} candidates")
    if res.data:
        for c in res.data[:3]:
            print(f"  {c.get('name', 'N/A')} - {c.get('party', 'N/A')}")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")

# Test 3: Try to list constituencies
print("\n--- Test 3: List constituencies ---")
try:
    res = client.table("constituencies").select("*").limit(3).execute()
    print(f"Success! Found {len(res.data)} constituencies")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
