
from src.ambassadors import create_referral_code


def test_referral_code_has_name_prefix():
    code = create_referral_code("Ashish Singh")
    assert code.startswith("ASHISH-")
    assert len(code.split("-")[1]) == 6


def test_referral_codes_are_unique_in_sample():
    codes = {
        create_referral_code("Ashish Singh")
        for _ in range(100)
    }
    assert len(codes) == 100
