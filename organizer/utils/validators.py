import re

def validate_phone(phone: str) -> str:
    """
    Validates that the phone number contains only allowed characters.
    Allowed: digits, plus sign, minus sign, parentheses, and spaces.
    Raises ValueError if invalid.
    """
    pattern = r"^[\d\+\-\(\)\s]+$"
    if not re.fullmatch(pattern, phone):
        raise ValueError(f"Invalid phone number format: '{phone}'")
    return phone
