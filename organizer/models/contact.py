from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
from organizer.utils.validators import validate_phone, validate_email, capitalize_name
from organizer.utils.exceptions import ValidationError


@dataclass
class Contact:
    """Represents a single contact entry with optional personal and contact details.

    Attributes:
        name (str): First name of the contact (required).
        last_name (Optional[str]): Last name of the contact.
        company (Optional[str]): Company or organization the contact is associated with.
        phone (Optional[str]): Phone number of the contact, validated for format.
        address (Optional[str]): Address or location of the contact.
        birthday (Optional[date]): Birthday of the contact as a `date` object.
        email (Optional[str]): Email address of the contact, validated for format.
        last_modified (datetime): Timestamp of the last modification to the contact.
    """

    name: str
    last_name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    birthday: Optional[date] = None
    email: Optional[str] = None
    last_modified: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validates and formats fields after initialization.

        Raises:
            ValidationError: If required fields are invalid.
        """
        if not self.name or not self.name.strip():
            raise ValidationError("Contact name cannot be empty or None.")
        self.name = capitalize_name(self.name.strip())

        self.last_name = capitalize_name(self.last_name.strip()) if self.last_name else None
        self.phone = validate_phone(self.phone) if self.phone else None
        self.email = validate_email(self.email) if self.email else None
        self.address = self.address.strip() if self.address else None
        self.company = self.company.strip() if self.company else None

        self.update_modified_time()

    def full_name(self) -> str:
        """Returns the full name of the contact.

        Returns:
            str: A concatenation of name and last name, trimmed of extra spaces.
        """
        return f"{self.name} {self.last_name or ''}".strip()

    def update_modified_time(self) -> None:
        """Updates the `last_modified` field to the current timestamp."""
        self.last_modified = datetime.now()
