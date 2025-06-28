import re
from email.utils import parseaddr


def validate_phone(phone: str) -> str:
    """Validates the phone number format.

    The phone number may include digits, plus signs, minus signs, parentheses, and spaces.

    Args:
        phone (str): The phone number to validate.

    Returns:
        str: The validated phone number.

    Raises:
        ValueError: If the phone number format is invalid.
    """
    pattern = r"^[\d\+\-\(\)\s]+$"
    if not re.fullmatch(pattern, phone):
        raise ValueError(f"Invalid phone number format: '{phone}'")
    return phone


def validate_email(email: str) -> str:
    """Validates the email address format.

    A valid email must contain an '@' and a domain suffix like '.com'.

    Args:
        email (str): The email address to validate.

    Returns:
        str: The validated email address.

    Raises:
        ValueError: If the email address format is invalid.
    """
    name, addr = parseaddr(email)
    if '@' not in addr or '.' not in addr.split('@')[-1]:
        raise ValueError(f"Invalid email address format: '{email}'")
    return email


def capitalize_name(name: str) -> str:
    """Capitalizes the first letter of a name and trims whitespace.

    Args:
        name (str): The name to capitalize.

    Returns:
        str: The capitalized name.
    """
    return name.strip().capitalize() if name else name


def normalize_text(text: str) -> str:
    """Normalizes text for consistent comparison.

    Converts text to lowercase and removes all non-alphanumeric characters.

    Args:
        text (str): The text to normalize.

    Returns:
        str: The normalized text.
    """
    return re.sub(r'\W+', '', text.lower())
