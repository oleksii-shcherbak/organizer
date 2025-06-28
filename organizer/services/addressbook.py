from typing import Optional, List
from datetime import date
from organizer.models.contact import Contact
from organizer.utils.validators import normalize_text, validate_phone, validate_email, capitalize_name


class AddressBook:
    def __init__(self) -> None:
        self._contacts: dict[str, Contact] = {}

    def add(self, contact: Contact) -> None:
        key = normalize_text(contact.name)
        self._contacts[key] = contact

    def get(self, name: str) -> Optional[Contact]:
        key = normalize_text(name)
        return self._contacts.get(key)

    def delete(self, name: str) -> bool:
        key = normalize_text(name)
        return self._contacts.pop(key, None) is not None

    def edit(self, name: str, updated_data: dict) -> bool:
        normalized_name = normalize_text(name)
        contact = self._contacts.get(normalized_name)
        if not contact:
            return False

        new_name = updated_data.get("name")
        if new_name:
            new_name = capitalize_name(new_name)
            new_normalized = normalize_text(new_name)

            if new_normalized != normalized_name:
                self._contacts.pop(normalized_name)
                contact.name = new_name
                self._contacts[new_normalized] = contact
            else:
                contact.name = new_name

        if "last_name" in updated_data:
            contact.last_name = capitalize_name(updated_data["last_name"])

        if "company" in updated_data:
            contact.company = updated_data["company"]

        if "phone" in updated_data:
            contact.phone = validate_phone(updated_data["phone"])

        if "address" in updated_data:
            contact.address = updated_data["address"]

        if "email" in updated_data:
            contact.email = validate_email(updated_data["email"])

        if "birthday" in updated_data:
            contact.birthday = updated_data["birthday"]

        contact.update_modified_time()
        return True

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
