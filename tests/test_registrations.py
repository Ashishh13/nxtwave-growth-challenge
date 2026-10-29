
import pytest

from src.registrations import register_student


def test_rejects_short_name():
    with pytest.raises(ValueError, match="full name"):
        register_student(
            full_name="A",
            email="student@example.com",
            college="Example Engineering College",
            is_final_year=True,
        )


def test_rejects_invalid_email():
    with pytest.raises(ValueError, match="valid email"):
        register_student(
            full_name="Test Student",
            email="not-an-email",
            college="Example Engineering College",
            is_final_year=True,
        )


def test_rejects_missing_college():
    with pytest.raises(ValueError, match="college name"):
        register_student(
            full_name="Test Student",
            email="student@example.com",
            college=" ",
            is_final_year=True,
        )


def test_rejects_non_final_year_student():
    with pytest.raises(ValueError, match="final-year"):
        register_student(
            full_name="Test Student",
            email="student@example.com",
            college="Example Engineering College",
            is_final_year=False,
        )
