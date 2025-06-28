from dataclasses import dataclass
from datetime import date
from typing import Optional
from organizer.utils.validators import validate_phone, validate_email, capitalize_name


@dataclass
class Contact:
    name: str
    last_name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    birthday: Optional[date] = None
    email: Optional[str] = None

    def __post_init__(self):
        self.phone = validate_phone(self.phone) if self.phone else self.phone
        self.email = validate_email(self.email) if self.email else self.email
        self.name = capitalize_name(self.name) if self.name else self.name
        self.last_name = capitalize_name(self.last_name) if self.last_name else self.last_name

    def full_name(self) -> str:
        return f"{self.name} {self.last_name or ''}".strip()
