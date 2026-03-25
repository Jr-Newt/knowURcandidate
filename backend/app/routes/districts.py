from fastapi import APIRouter
from app.services.supabase_service import get_all_districts

router = APIRouter(tags=["districts"])


@router.get("/districts")
def list_districts():
    """Get all Kerala districts."""
    districts = get_all_districts()
    return {"districts": districts}
