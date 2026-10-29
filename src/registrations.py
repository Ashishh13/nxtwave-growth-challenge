
import re

from src.db import get_supabase_client


def register_student(
    full_name: str,
    email: str,
    college: str,
    is_final_year: bool,
    referral_code: str = "",
) -> dict:
    """Validate and save a student's workshop registration."""

    full_name = full_name.strip()
    email = email.strip().lower()
    college = college.strip()
    referral_code = referral_code.strip().upper()

    if len(full_name) < 2:
        raise ValueError("Please enter your full name.")

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ValueError("Please enter a valid email address.")

    if len(college) < 2:
        raise ValueError("Please enter your college name.")

    if not is_final_year:
        raise ValueError(
            "This workshop campaign is intended for final-year engineering students."
        )

    client = get_supabase_client()

    # Validate the referral code before saving the registration.
    if referral_code:
        ambassador_result = (
            client.table("ambassadors")
            .select("referral_code")
            .eq("referral_code", referral_code)
            .limit(1)
            .execute()
        )

        if not ambassador_result.data:
            raise ValueError(
                "That referral code was not found. Check the code or leave it blank."
            )

    registration = {
        "full_name": full_name,
        "email": email,
        "college": college,
        "is_final_year": is_final_year,
        "referral_code": referral_code or None,
        "source": "ambassador" if referral_code else "direct",
    }

    try:
        response = (
            client.table("registrations")
            .insert(registration)
            .execute()
        )
    except Exception as exc:
        error_text = str(exc).lower()

        if "23505" in error_text or "duplicate key" in error_text:
            raise ValueError(
                "This email is already registered for the workshop."
            ) from exc

        if "23503" in error_text or "foreign key" in error_text:
            raise ValueError(
                "The referral code is invalid. Please check it and try again."
            ) from exc

        raise

    if not response.data:
        raise RuntimeError("The registration was not saved. Please try again.")

    return response.data[0]
