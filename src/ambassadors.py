
import re
import secrets
import string

from src.db import get_supabase_client


def create_referral_code(name: str) -> str:
    """Generate a readable referral code from a name."""
    prefix = re.sub(r"[^A-Z0-9]", "", name.upper())[:6]
    if not prefix:
        prefix = "CAMPUS"

    suffix = "".join(
        secrets.choice(string.ascii_uppercase + string.digits)
        for _ in range(6)
    )
    return f"{prefix}-{suffix}"


def register_ambassador(
    full_name: str,
    email: str,
    college: str,
) -> dict:
    """Validate and save an ambassador to Supabase."""
    full_name = full_name.strip()
    email = email.strip().lower()
    college = college.strip()

    if len(full_name) < 2:
        raise ValueError("Enter a valid full name.")

    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Enter a valid email address.")

    if len(college) < 2:
        raise ValueError("Enter a valid college name.")

    client = get_supabase_client()

    # Retry if a randomly generated referral code collides.
    for _ in range(3):
        referral_code = create_referral_code(full_name)

        try:
            response = (
                client.table("ambassadors")
                .insert({
                    "full_name": full_name,
                    "email": email,
                    "college": college,
                    "referral_code": referral_code,
                })
                .execute()
            )
            if response.data:
                return response.data[0]

        except Exception as exc:
            # Duplicate email should not be retried with another code.
            message = str(exc).lower()
            if "email" in message or "23505" in message:
                raise ValueError(
                    "This email may already be registered. "
                    "Please check your details."
                ) from exc
            raise

    raise RuntimeError(
        "Could not create a referral code. Please try again."
    )
