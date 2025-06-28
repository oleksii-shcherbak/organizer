import re
from email.utils import parseaddr

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

def validate_email(email: str) -> str:
    """
    Validates that the email is in a proper format.
    A valid email must contain '@' and a domain suffix like '.com'.
    Raises ValueError if invalid.
    """
    name, addr = parseaddr(email)
    if '@' not in addr or '.' not in addr.split('@')[-1]:
        raise ValueError(f"Invalid email address format: '{email}'")
    return email

def capitalize_name(name: str) -> str:
    """
    Capitalizes the first letter of the name and strips leading/trailing whitespace.
    """
    return name.strip().capitalize() if name else name

def normalize_text(text: str) -> str:
    """
    Normalizes text for consistent comparison:
    - Converts to lowercase
    - Removes non-alphanumeric characters
    """
    return re.sub(r'\W+', '', text.lower())
