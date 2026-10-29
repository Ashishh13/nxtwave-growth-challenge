
import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import Client, create_client

# Load .env from the project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def get_supabase_client() -> Client:
    """Create a Supabase client using local environment settings."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError(
            "Supabase settings are missing. "
            "Check the project's .env file."
        )

    return create_client(url, key)


def get_campaign_settings() -> dict:
    """Fetch the non-sensitive campaign configuration."""
    client = get_supabase_client()

    response = (
        client.table("campaign_settings")
        .select("registration_target, budget_inr, duration_days")
        .eq("id", 1)
        .single()
        .execute()
    )

    if not response.data:
        raise RuntimeError("Campaign settings were not found.")

    return response.data
