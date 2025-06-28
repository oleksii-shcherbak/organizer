from typing import Optional, List
from datetime import date
from organizer.models.contact import Contact
from organizer.utils.validators import normalize_text


class AddressBook:
    def __init__(self) -> None:
        self._contacts: dict[str, Contact] = {}

    def add(self, contact: Contact) -> None:
        self._contacts[contact.name] = contact

    def get(self, name: str) -> Optional[Contact]:
        return self._contacts.get(name)

    def delete(self, name: str) -> bool:
        return self._contacts.pop(name, None) is not None

    def edit(self, name: str, updated: Contact) -> bool:
        if name in self._contacts:
            self._contacts[name] = updated
            return True
        return False

    def search(self, query: str) -> List[Contact]:
        results = []
        query_norm = normalize_text(query)
        for contact in self._contacts.values():
            fields = [
                contact.name,
                contact.last_name,
                contact.company,
                contact.phone,
                contact.address,
                contact.email,
                contact.birthday.strftime("%d-%m-%Y") if contact.birthday else ""
            ]
            combined = " ".join(field or "" for field in fields)
            combined_norm = normalize_text(combined)
            if query_norm in combined_norm:
                results.append(contact)
        return results

    def all(self) -> List[Contact]:
        return list(self._contacts.values())

    def sort(self, by: str = "name") -> List[Contact]:
        if by == "name":
            return sorted(self._contacts.values(), key=lambda c: c.full_name().lower())
        elif by == "updated":
            return sorted(self._contacts.values(), key=lambda c: c.last_modified, reverse=True)
        else:
            raise ValueError("Unsupported sort key. Use 'name' or 'updated'.")

    def get_upcoming_birthdays(self, days: int = 7) -> List[Contact]:
        today = date.today()
        upcoming = []
        for contact in self._contacts.values():
            if contact.birthday:
                try:
                    bday_this_year = contact.birthday.replace(year=today.year)
                except ValueError:
                    continue  # skip invalid dates like Feb 29 on non-leap years
                delta = (bday_this_year - today).days
                if 0 <= delta <= days:
                    upcoming.append(contact)
        return upcoming
