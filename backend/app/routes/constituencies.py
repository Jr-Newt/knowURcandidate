from fastapi import APIRouter, Query
from app.services.supabase_service import get_constituencies_by_district

router = APIRouter(tags=["constituencies"])


@router.get("/constituencies")
def list_constituencies(district: str = Query(..., description="District name")):
    """Get constituencies within a district."""
    constituencies = get_constituencies_by_district(district)
    return {"constituencies": constituencies}
