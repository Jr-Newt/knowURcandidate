"""
Loads the scraped 2026 Kerala MLA candidate data into Supabase.
1. Clears existing mock data
2. Inserts new Districts, Constituencies, and Candidates
"""
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

env_path = Path(__file__).parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

client = create_client(SUPABASE_URL, SUPABASE_KEY)
DATA_FILE = Path(__file__).parent / "output" / "candidates_2026_raw.json"

def calculate_scores(candidate):
    """Calculate the simple 0-1 scores as used in the website."""
    # Criminal score: 1.0 = no cases, lower = more cases
    cases = candidate.get("criminal_cases", 0)
    serious = candidate.get("serious_cases", 0)
    crim_score = max(0.0, 1.0 - (cases * 0.1) - (serious * 0.2))

    # Education score: simple heuristic
    edu = candidate.get("education", "").lower()
    if "doctorate" in edu:
        edu_score = 1.0
    elif "post graduate" in edu:
        edu_score = 0.9
    elif "graduate" in edu:
        edu_score = 0.8
    elif "12th" in edu:
        edu_score = 0.6
    elif "10th" in edu:
        edu_score = 0.5
    else:
        edu_score = 0.4

    # Asset score: log scale roughly
    assets = candidate.get("assets", 0)
    if assets == 0:
        asset_score = 0.5
    else:
        # Scale 1 lakh to 100 crore roughly between 0.2 to 1.0
        asset_score = min(1.0, max(0.1, (len(str(assets)) - 4) / 5))

    return {
        "education_score": round(edu_score, 2),
        "criminal_score": round(crim_score, 2),
        "asset_score": round(asset_score, 2),
        "experience_score": 0.5  # default
    }

def load_data():
    if not DATA_FILE.exists():
        print(f"Error: {DATA_FILE} not found.")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    print(f"Loading {len(candidates)} candidates to Supabase...")

    # 1. Clear existing candidate data
    print("Clearing old candidate data...")
    client.table("candidates").delete().neq("id", 0).execute()
    
    # 2. Extract unique constituencies
    # In full reality, we'd map districts accurately. For the scraped subset,
    # we'll create them or map them to a default district if unknown.
    # First ensure at least one district exists for fallback
    dist_res = client.table("districts").select("id").limit(1).execute()
    if not dist_res.data:
        client.table("districts").insert({"name": "Kerala Default"}).execute()
        dist_res = client.table("districts").select("id").limit(1).execute()
    default_district_id = dist_res.data[0]["id"]

    # 3. Insert candidates and constituencies
    const_cache = {}
    success_count = 0
    
    for c in candidates:
        name = c.get("name")
        if not name or name.startswith("Status"):
            continue

        const_name = c.get("constituency")
        if not const_name:
            const_name = "Unknown"

        # Get or create constituency
        if const_name not in const_cache:
            res = client.table("constituencies").select("id").eq("name", const_name).execute()
            if res.data:
                const_cache[const_name] = res.data[0]["id"]
            else:
                ins = client.table("constituencies").insert({
                    "name": const_name,
                    "district_id": default_district_id
                }).execute()
                const_cache[const_name] = ins.data[0]["id"]

        const_id = const_cache[const_name]
        scores = calculate_scores(c)

        db_cand = {
            "name": name,
            "constituency_id": const_id,
            "party": c.get("party", "Unknown"),
            "education": c.get("education", "Unknown"),
            "criminal_cases": c.get("criminal_cases", 0),
            "serious_cases": c.get("serious_cases", 0),
            "assets": c.get("assets", 0),
            "liabilities": c.get("liabilities", 0),
            "profession": c.get("profession", "Unknown"),
            "age": c.get("age"),
            "affidavit_link": c.get("affidavit_link", ""),
            "education_score": scores["education_score"],
            "criminal_score": scores["criminal_score"],
            "asset_score": scores["asset_score"],
            "experience_score": scores["experience_score"]
        }

        try:
            client.table("candidates").insert(db_cand).execute()
            success_count += 1
            print(f"  Inserted: {name} ({c.get('party')})")
        except Exception as e:
            print(f"  Failed to insert {name}: {e}")

    print(f"\nSuccessfully loaded {success_count} candidates!")

if __name__ == "__main__":
    load_data()
