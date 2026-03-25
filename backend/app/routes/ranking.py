from fastapi import APIRouter
from app.models import RankRequest, RankedCandidate
from app.services.supabase_service import get_candidates_for_ranking
from app.services.ranking_engine import compute_ranking

router = APIRouter(tags=["ranking"])


@router.post("/rank", response_model=dict)
def rank_candidates(request: RankRequest):
    """
    Dynamically rank candidates based on user-provided weights.

    Rankings are computed at runtime and NEVER stored in the database.
    The response includes per-candidate score breakdown for full transparency.

    Weight behavior:
    - Higher education weight → educated candidates rank higher
    - Higher criminal weight → candidates with fewer cases rank higher
    - Higher experience weight → more experienced candidates rank higher
    - Higher assets weight → wealthier candidates rank higher
    """
    # Fetch candidates from DB (with normalized scores, no pre-computed rank)
    candidates = get_candidates_for_ranking(
        district=request.district,
        constituency=request.constituency,
    )

    # Compute ranking dynamically
    ranked = compute_ranking(candidates, request.weights)

    return {
        "ranked_candidates": [r.model_dump() for r in ranked],
        "total": len(ranked),
        "weights_used": {
            "education": request.weights.education,
            "criminal": request.weights.criminal,
            "experience": request.weights.experience,
            "assets": request.weights.assets,
        },
        "disclaimer": "Ranking is based on user-selected preferences and does not represent any official or editorial position.",
    }
