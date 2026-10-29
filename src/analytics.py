
from src.db import get_supabase_client


def get_campaign_analytics() -> dict:
    """Fetch aggregate campaign analytics without exposing student records."""
    client = get_supabase_client()

    response = client.rpc("get_campaign_analytics").execute()

    if not response.data:
        return {
            "total_registrations": 0,
            "by_source": [],
            "daily_registrations": [],
            "by_ambassador": [],
        }

    return response.data
