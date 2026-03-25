"""
Dynamic Ranking Engine

Computes candidate rankings at runtime based on user-provided weights.
Rankings are NEVER stored in the database — always computed fresh per request.

Formula:
    Score = (education_score × w_education) +
            (criminal_score × w_criminal) +
            (experience_score × w_experience) +
            (asset_score × w_assets)

Criminal score is stored inverted: 1.0 = no cases (best), 0.0 = many cases (worst).
This ensures that increasing criminal weight always pushes clean candidates higher.
"""

from app.models import RankWeights, ScoreBreakdown, RankedCandidate


def compute_ranking(candidates: list[dict], weights: RankWeights) -> list[RankedCandidate]:
    """
    Compute dynamic ranking for a list of candidates based on user weights.

    Args:
        candidates: List of candidate dicts from Supabase with normalized scores
        weights: User-provided weights for each factor

    Returns:
        Sorted list of RankedCandidate objects (highest score first)
    """
    # Normalize weights to sum to 1.0 (prevents gaming)
    total_weight = weights.education + weights.criminal + weights.experience + weights.assets
    if total_weight == 0:
        # Equal weights if all zeros
        w_edu = w_crim = w_exp = w_asset = 0.25
    else:
        w_edu = weights.education / total_weight
        w_crim = weights.criminal / total_weight
        w_exp = weights.experience / total_weight
        w_asset = weights.assets / total_weight

    ranked = []
    for c in candidates:
        edu_score = c.get("education_score", 0.0) or 0.0
        crim_score = c.get("criminal_score", 1.0) or 1.0
        exp_score = c.get("experience_score", 0.0) or 0.0
        asset_score = c.get("asset_score", 0.0) or 0.0

        # Weighted score computation
        breakdown = ScoreBreakdown(
            education=round(edu_score * w_edu, 4),
            criminal=round(crim_score * w_crim, 4),
            experience=round(exp_score * w_exp, 4),
            assets=round(asset_score * w_asset, 4),
        )

        total_score = round(
            breakdown.education + breakdown.criminal + breakdown.experience + breakdown.assets,
            4,
        )

        ranked.append(
            RankedCandidate(
                id=c["id"],
                name=c["name"],
                party=c.get("party"),
                constituency_name=c.get("constituency_name"),
                district_name=c.get("district_name"),
                total_score=total_score,
                breakdown=breakdown,
                education=c.get("education"),
                criminal_cases=c.get("criminal_cases", 0),
                serious_cases=c.get("serious_cases", 0),
                assets=c.get("assets", 0),
                liabilities=c.get("liabilities", 0),
                profession=c.get("profession"),
                age=c.get("age"),
            )
        )

    # Sort descending by total score
    ranked.sort(key=lambda x: x.total_score, reverse=True)
    return ranked
