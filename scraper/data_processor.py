"""
Data Processor — Normalize raw candidate data into 0-1 scores.
"""

import json
from pathlib import Path

# Education level mapping → score (0.0 to 1.0)
EDUCATION_SCORES = {
    "illiterate": 0.0,
    "literate": 0.1,
    "5th pass": 0.15,
    "8th pass": 0.2,
    "10th pass": 0.25,
    "sslc": 0.25,
    "12th pass": 0.35,
    "hsc": 0.35,
    "diploma": 0.4,
    "graduate": 0.6,
    "law graduate": 0.7,
    "professional graduate": 0.7,
    "post graduate": 0.8,
    "doctorate": 1.0,
    "phd": 1.0,
}


def normalize_education(education_str: str) -> float:
    """Convert education string to a 0-1 score."""
    if not education_str:
        return 0.0
    key = education_str.strip().lower()
    # Fuzzy match
    for label, score in EDUCATION_SCORES.items():
        if label in key:
            return score
    return 0.3  # Default for unrecognized


def normalize_criminal(total_cases: int, serious_cases: int) -> float:
    """
    Convert criminal record to a 0-1 score.
    1.0 = no cases (best), 0.0 = many serious cases (worst).
    Serious cases are weighted 2x.
    """
    if total_cases == 0 and serious_cases == 0:
        return 1.0
    weighted = total_cases + (serious_cases * 2)
    # Diminishing penalty: score drops fast initially
    score = max(0.0, 1.0 - (weighted * 0.15))
    return round(score, 4)


def normalize_assets(assets: int, constituency_assets: list[int]) -> float:
    """
    Normalize assets relative to constituency peers.
    Returns 0-1 where 1.0 = highest assets in constituency.
    """
    if not constituency_assets or max(constituency_assets) == 0:
        return 0.0
    max_asset = max(constituency_assets)
    return round(min(1.0, assets / max_asset), 4) if max_asset > 0 else 0.0


def estimate_experience(profession: str, age: int) -> float:
    """
    Estimate experience score from profession and age.
    Heuristic-based since we often don't have explicit experience data.
    """
    score = 0.0

    # Age component (older = more likely to have experience)
    if age:
        if age >= 60:
            score += 0.4
        elif age >= 50:
            score += 0.3
        elif age >= 40:
            score += 0.2
        elif age >= 30:
            score += 0.1

    # Profession component
    if profession:
        prof_lower = profession.lower()
        political_keywords = ["politician", "political worker", "mla", "mp", "minister", "councillor"]
        professional_keywords = ["advocate", "lawyer", "doctor", "engineer", "professor", "teacher"]
        business_keywords = ["business", "industrialist", "entrepreneur"]

        if any(kw in prof_lower for kw in political_keywords):
            score += 0.5
        elif any(kw in prof_lower for kw in professional_keywords):
            score += 0.35
        elif any(kw in prof_lower for kw in business_keywords):
            score += 0.3
        else:
            score += 0.2

    return round(min(1.0, score), 4)


def process_candidates(raw_candidates: list) -> list:
    """
    Process raw candidate data and add normalized scores.

    Args:
        raw_candidates: List of dicts from the scraper

    Returns:
        List of processed candidate dicts with scores
    """
    # Group by constituency for relative normalization
    by_constituency = {}
    for c in raw_candidates:
        const = c.get("constituency", "Unknown")
        by_constituency.setdefault(const, []).append(c)

    processed = []
    for constituency, candidates in by_constituency.items():
        # Get all assets for constituency-level normalization
        all_assets = [c.get("assets", 0) for c in candidates]

        for c in candidates:
            c["education_score"] = normalize_education(c.get("education", ""))
            c["criminal_score"] = normalize_criminal(
                c.get("criminal_cases", 0),
                c.get("serious_cases", 0),
            )
            c["asset_score"] = normalize_assets(c.get("assets", 0), all_assets)
            c["experience_score"] = estimate_experience(
                c.get("profession", ""),
                int(c.get("age", 0)) if c.get("age") else 0,
            )
            processed.append(c)

    return processed


if __name__ == "__main__":
    input_file = Path(__file__).parent / "output" / "candidates_raw.json"
    if input_file.exists():
        with open(input_file) as f:
            raw = json.load(f)
        result = process_candidates(raw)
        output_file = Path(__file__).parent / "output" / "candidates_processed.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Processed {len(result)} candidates → {output_file}")
    else:
        print(f"Input file not found: {input_file}")
