from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Contact:
    name: str
    last_name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    birthday: Optional[date] = None
    email: Optional[str] = None

    def full_name(self) -> str:
        return f"{self.name} {self.last_name or ''}".strip()
