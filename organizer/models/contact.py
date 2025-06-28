from dataclasses import dataclass, field
from datetime import date, datetime
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
    last_modified: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        self.phone = validate_phone(self.phone) if self.phone else self.phone
        self.email = validate_email(self.email) if self.email else self.email
        self.name = capitalize_name(self.name) if self.name else self.name
        self.last_name = capitalize_name(self.last_name) if self.last_name else self.last_name
        self.update_modified_time()

    def full_name(self) -> str:
        return f"{self.name} {self.last_name or ''}".strip()

    def update_modified_time(self) -> None:
        self.last_modified = datetime.now()
