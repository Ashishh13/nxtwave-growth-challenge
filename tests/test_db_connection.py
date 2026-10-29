
from src.db import get_campaign_settings


def main():
    settings = get_campaign_settings()

    print("Supabase connection successful!")
    print(f"Registration target: {settings['registration_target']}")
    print(f"Campaign budget: ₹{settings['budget_inr']}")
    print(f"Campaign duration: {settings['duration_days']} days")


if __name__ == "__main__":
    main()
