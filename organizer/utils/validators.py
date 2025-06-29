import re
from email.utils import parseaddr
from organizer.utils.exceptions import ValidationError


def validate_phone(phone: str) -> str:
    """Validates the phone number format.

    The phone number may include digits, plus signs, minus signs,
    parentheses, and spaces. It must match the allowed pattern.

    Args:
        phone (str): The phone number to validate.

    Returns:
        str: The validated phone number.

    Raises:
        ValidationError: If the phone number format is invalid.
    """
    pattern = r"^[\d\+\-\(\)\s]+$"
    if not phone or not re.fullmatch(pattern, phone):
        raise ValidationError(f"Invalid phone number format: '{phone}'")
    return phone


def validate_email(email: str) -> str:
    """Validates the email address format.

    A valid email must contain '@' and a domain with '.'.

    Args:
        email (str): The email address to validate.

    Returns:
        str: The validated email address.

    Raises:
        ValidationError: If the email address format is invalid.
    """
    name, addr = parseaddr(email)
    if not email or '@' not in addr or '.' not in addr.split('@')[-1]:
        raise ValidationError(f"Invalid email address format: '{email}'")
    return email


def capitalize_name(name: str) -> str:
    """Capitalizes the first letter of a name and trims whitespace.

    Args:
        name (str): The name to capitalize.

    Returns:
        str: The capitalized name.

    Raises:
        ValidationError: If the name is None or empty.
    """
    if not name or not name.strip():
        raise ValidationError("Name cannot be empty or None.")
    return name.strip().capitalize()


def normalize_text(text: str) -> str:
    """Normalizes text for consistent comparison.

    Converts text to lowercase and removes all non-alphanumeric characters.

    Args:
        text (str): The text to normalize.

    Returns:
        str: The normalized text.
    """
    return re.sub(r'\W+', '', text.lower())
