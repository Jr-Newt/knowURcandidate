"""
Supabase Loader — UPSERT processed data into Supabase tables.
Loads candidate data and news into the database, avoiding duplicates.
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(Path(__file__).parent.parent / "backend" / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

MAPPINGS_FILE = Path(__file__).parent / "mappings" / "constituency_district.json"


def get_supabase():
    """Initialize Supabase client."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("Set SUPABASE_URL and SUPABASE_KEY in backend/.env")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def load_mappings() -> dict:
    """Load constituency-to-district mapping."""
    with open(MAPPINGS_FILE) as f:
        data = json.load(f)
    mapping = {}
    for district in data["districts"]:
        for constituency in district["constituencies"]:
            mapping[constituency.lower()] = district["name"]
    return mapping


def upsert_districts_and_constituencies(supabase, mappings_data: dict):
    """Seed districts and constituencies from the mapping file."""
    with open(MAPPINGS_FILE) as f:
        data = json.load(f)

    for district_info in data["districts"]:
        district_name = district_info["name"]
        # Upsert district
        supabase.table("districts").upsert(
            {"name": district_name},
            on_conflict="name",
        ).execute()

        # Get district ID
        res = supabase.table("districts").select("id").eq("name", district_name).execute()
        if not res.data:
            continue
        district_id = res.data[0]["id"]

        # Upsert constituencies
        for const_name in district_info["constituencies"]:
            supabase.table("constituencies").upsert(
                {"name": const_name, "district_id": district_id},
                on_conflict="name,district_id",
            ).execute()

    print("Districts and constituencies loaded.")


def upsert_candidates(supabase, candidates: list, mapping: dict):
    """UPSERT candidates into the database."""
    for c in candidates:
        # Resolve constituency ID
        const_name = c.get("constituency", "")
        district_name = mapping.get(const_name.lower(), "")

        # Find constituency ID
        query = supabase.table("constituencies").select("id, district_id")
        if const_name:
            query = query.eq("name", const_name)
        res = query.execute()

        if not res.data:
            print(f"  Skipping {c.get('name')} — constituency '{const_name}' not found")
            continue

        constituency_id = res.data[0]["id"]

        record = {
            "name": c.get("name", ""),
            "constituency_id": constituency_id,
            "party": c.get("party", ""),
            "education": c.get("education", ""),
            "criminal_cases": c.get("criminal_cases", 0),
            "serious_cases": c.get("serious_cases", 0),
            "assets": c.get("assets", 0),
            "liabilities": c.get("liabilities", 0),
            "profession": c.get("profession", ""),
            "age": c.get("age"),
            "affidavit_link": c.get("affidavit_link", ""),
            "education_score": c.get("education_score", 0.0),
            "criminal_score": c.get("criminal_score", 1.0),
            "asset_score": c.get("asset_score", 0.0),
            "experience_score": c.get("experience_score", 0.0),
        }

        supabase.table("candidates").upsert(
            record,
            on_conflict="name,constituency_id,party",
        ).execute()

    print(f"Upserted {len(candidates)} candidates.")


def upsert_news(supabase, news_data: dict, candidates_lookup: dict):
    """UPSERT news articles for candidates."""
    count = 0
    for candidate_name, articles in news_data.items():
        candidate_id = candidates_lookup.get(candidate_name)
        if not candidate_id:
            print(f"  Skipping news for '{candidate_name}' — candidate not found in DB")
            continue

        for article in articles:
            record = {
                "candidate_id": candidate_id,
                "title": article.get("title", ""),
                "source": article.get("source", ""),
                "published_date": article.get("published_date"),
                "url": article.get("url", ""),
                "summary": article.get("summary"),
            }
            supabase.table("candidate_news").upsert(
                record,
                on_conflict="url",
            ).execute()
            count += 1

    print(f"Upserted {count} news articles.")


def run_full_load():
    """Full pipeline: load districts, constituencies, candidates, news."""
    supabase = get_supabase()
    mapping = load_mappings()

    # 1. Seed geography data
    upsert_districts_and_constituencies(supabase, mapping)

    # 2. Load candidates
    candidates_file = Path(__file__).parent / "output" / "candidates_processed.json"
    if candidates_file.exists():
        with open(candidates_file) as f:
            candidates = json.load(f)
        upsert_candidates(supabase, candidates, mapping)
    else:
        print(f"No processed candidates file found at {candidates_file}")

    # 3. Build candidate name → ID lookup
    all_candidates = supabase.table("candidates").select("id, name").execute()
    lookup = {c["name"]: c["id"] for c in all_candidates.data}

    # 4. Load news
    news_file = Path(__file__).parent / "output" / "news_raw.json"
    if news_file.exists():
        with open(news_file) as f:
            news_data = json.load(f)
        upsert_news(supabase, news_data, lookup)
    else:
        print(f"No news file found at {news_file}")

    print("Full load complete!")


if __name__ == "__main__":
    run_full_load()
