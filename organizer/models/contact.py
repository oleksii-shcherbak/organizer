from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from organizer.utils.validators import validate_phone


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
        if self.phone:
            self.phone = validate_phone(self.phone)

    def full_name(self) -> str:
        return f"{self.name} {self.last_name or ''}".strip()
