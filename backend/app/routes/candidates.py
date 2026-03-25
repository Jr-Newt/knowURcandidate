from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.supabase_service import (
    get_candidates,
    get_candidate_by_id,
    get_candidate_news,
)

router = APIRouter(tags=["candidates"])


@router.get("/candidates")
def list_candidates(
    district: Optional[str] = Query(None, description="Filter by district name"),
    constituency: Optional[str] = Query(None, description="Filter by constituency name"),
):
    """Get candidates with optional district/constituency filters."""
    candidates = get_candidates(district=district, constituency=constituency)
    return {"candidates": candidates}


@router.get("/candidate/{candidate_id}")
def get_candidate(candidate_id: int):
    """Get full details for a single candidate."""
    candidate = get_candidate_by_id(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return {"candidate": candidate}


@router.get("/candidate/{candidate_id}/news")
def get_news(candidate_id: int):
    """Get news articles for a candidate."""
    news = get_candidate_news(candidate_id)
    return {"news": news}
