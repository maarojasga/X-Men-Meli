from fastapi import APIRouter
from schemas.stats import StatsResponse
from services.stats_service import get_stats

router = APIRouter()

@router.get("/stats", response_model=StatsResponse)
async def stats():
    """
    Endpoint to retrieve statistics on recorded DNA sequences.

    Returns:
        StatsResponse: An object containing statistics including the count of mutant and human records,
                       as well as the ratio of mutants to total records.
    """
    return get_stats()
