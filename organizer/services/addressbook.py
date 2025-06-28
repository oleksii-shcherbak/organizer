from typing import Optional, List
from datetime import date
from organizer.models.contact import Contact
from organizer.utils.validators import normalize_text, validate_phone, validate_email, capitalize_name


class AddressBook:
    def __init__(self) -> None:
        self._contacts: List[Contact] = []

    def add(self, contact: Contact) -> None:
        if not contact.name or not contact.name.strip():
            raise ValueError("Contact name cannot be empty or None.")
        key = normalize_text(contact.name)
        self._contacts.append(contact)

    def get(self, name: str) -> List[Contact]:
        key = normalize_text(name)
        return [c for c in self._contacts if normalize_text(c.name) == key]

    def delete(self, name: str) -> bool:
        key = normalize_text(name)
        for i, contact in enumerate(self._contacts):
            if normalize_text(contact.name) == key:
                del self._contacts[i]
                return True
        return False

    def edit(self, name: str, updated_data: dict) -> bool:
        key = normalize_text(name)
        for contact in self._contacts:
            if normalize_text(contact.name) == key:
                for field, value in updated_data.items():
                    if field == "name" and value:
                        contact.name = capitalize_name(value)
                    elif field == "last_name":
                        contact.last_name = capitalize_name(value) if value else None
                    elif field == "company":
                        contact.company = value
                    elif field == "phone":
                        contact.phone = validate_phone(value) if value else None
                    elif field == "address":
                        contact.address = value
                    elif field == "email":
                        contact.email = validate_email(value) if value else None
                    elif field == "birthday":
                        contact.birthday = value
                contact.update_modified_time()
                return True
        return False

    def search(self, query: str) -> List[Contact]:
        results = []
        query_norm = normalize_text(query)
        for contact in self._contacts:  # was: self._contacts.values()
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
        return self._contacts

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
