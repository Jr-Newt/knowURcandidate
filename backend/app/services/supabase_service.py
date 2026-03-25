from app.config import get_supabase


def get_all_districts():
    """Fetch all districts ordered by name."""
    supabase = get_supabase()
    response = supabase.table("districts").select("id, name").order("name").execute()
    return response.data


def get_constituencies_by_district(district_name: str):
    """Fetch constituencies for a given district name."""
    supabase = get_supabase()
    # First get the district ID
    district = (
        supabase.table("districts")
        .select("id")
        .eq("name", district_name)
        .execute()
    )
    if not district.data:
        return []
    district_id = district.data[0]["id"]
    response = (
        supabase.table("constituencies")
        .select("id, name, district_id")
        .eq("district_id", district_id)
        .order("name")
        .execute()
    )
    return response.data


def get_candidates(district: str = None, constituency: str = None):
    """Fetch candidates with optional district/constituency filters."""
    supabase = get_supabase()

    # Build query with joins
    query = supabase.table("candidates").select(
        "*, constituencies!inner(name, district_id, districts!inner(name))"
    )

    if constituency:
        query = query.eq("constituencies.name", constituency)
    if district:
        query = query.eq("constituencies.districts.name", district)

    response = query.order("name").execute()

    # Flatten the joined data
    candidates = []
    for row in response.data:
        candidate = {k: v for k, v in row.items() if k != "constituencies"}
        if row.get("constituencies"):
            candidate["constituency_name"] = row["constituencies"]["name"]
            if row["constituencies"].get("districts"):
                candidate["district_name"] = row["constituencies"]["districts"]["name"]
        candidates.append(candidate)

    return candidates


def get_candidate_by_id(candidate_id: int):
    """Fetch a single candidate with constituency and district info."""
    supabase = get_supabase()
    response = (
        supabase.table("candidates")
        .select("*, constituencies(name, district_id, districts(name))")
        .eq("id", candidate_id)
        .execute()
    )
    if not response.data:
        return None

    row = response.data[0]
    candidate = {k: v for k, v in row.items() if k != "constituencies"}
    if row.get("constituencies"):
        candidate["constituency_name"] = row["constituencies"]["name"]
        if row["constituencies"].get("districts"):
            candidate["district_name"] = row["constituencies"]["districts"]["name"]
    return candidate


def get_candidate_news(candidate_id: int):
    """Fetch news articles for a candidate."""
    supabase = get_supabase()
    response = (
        supabase.table("candidate_news")
        .select("*")
        .eq("candidate_id", candidate_id)
        .order("published_date", desc=True)
        .execute()
    )
    return response.data


def get_candidates_for_ranking(district: str = None, constituency: str = None):
    """Fetch candidates with their normalized scores for ranking computation."""
    supabase = get_supabase()

    query = supabase.table("candidates").select(
        "id, name, party, education, criminal_cases, serious_cases, assets, liabilities, "
        "profession, age, education_score, criminal_score, asset_score, experience_score, "
        "constituencies!inner(name, district_id, districts!inner(name))"
    )

    if constituency:
        query = query.eq("constituencies.name", constituency)
    if district:
        query = query.eq("constituencies.districts.name", district)

    response = query.execute()

    # Flatten
    candidates = []
    for row in response.data:
        candidate = {k: v for k, v in row.items() if k != "constituencies"}
        if row.get("constituencies"):
            candidate["constituency_name"] = row["constituencies"]["name"]
            if row["constituencies"].get("districts"):
                candidate["district_name"] = row["constituencies"]["districts"]["name"]
        candidates.append(candidate)

    return candidates
