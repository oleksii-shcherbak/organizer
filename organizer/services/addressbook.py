from typing import Optional, List
from datetime import date
from organizer.models.contact import Contact
from organizer.utils.validators import normalize_text, validate_phone, validate_email, capitalize_name


class AddressBook:
    """Manages a collection of Contact objects with operations like add, edit, delete, search, and sort."""

    def __init__(self) -> None:
        """Initializes an empty AddressBook."""
        self._contacts: List[Contact] = []

    def add(self, contact: Contact) -> None:
        """Adds a contact to the address book.

        Args:
            contact (Contact): The contact to add.

        Raises:
            ValueError: If the contact's name is empty or None.
        """
        if not contact.name or not contact.name.strip():
            raise ValueError("Contact name cannot be empty or None.")
        self._contacts.append(contact)

    def get(self, name: str) -> List[Contact]:
        """Retrieves all contacts with a given name.

        Args:
            name (str): The name to search for.

        Returns:
            List[Contact]: A list of matching contacts.
        """
        key = normalize_text(name)
        return [c for c in self._contacts if normalize_text(c.name) == key]

    def delete(self, name: str) -> bool:
        """Deletes the first contact found with the given name.

        Args:
            name (str): The name of the contact to delete.

        Returns:
            bool: True if a contact was deleted, False otherwise.
        """
        key = normalize_text(name)
        for i, contact in enumerate(self._contacts):
            if normalize_text(contact.name) == key:
                del self._contacts[i]
                return True
        return False

    def edit(self, name: str, updated_data: dict) -> bool:
        """Edits the first contact found with the given name.

        Args:
            name (str): The name of the contact to edit.
            updated_data (dict): Dictionary with fields to update.

        Returns:
            bool: True if a contact was updated, False otherwise.
        """
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
        """Searches for contacts that contain the query in any of their fields.

        Args:
            query (str): The search query.

        Returns:
            List[Contact]: A list of matching contacts.
        """
        results = []
        query_norm = normalize_text(query)
        for contact in self._contacts:
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
        """Returns all contacts in the address book.

        Returns:
            List[Contact]: A list of all contacts.
        """
        return self._contacts

    def sort(self, by: str = "name") -> List[Contact]:
        """Sorts the contact list by a specified key.

        Args:
            by (str): Sort key. Options are "name" or "updated".

        Returns:
            List[Contact]: A sorted list of contacts.

        Raises:
            ValueError: If an unsupported sort key is given.
        """
        if by == "name":
            return sorted(self._contacts, key=lambda c: c.full_name().lower())
        elif by == "updated":
            return sorted(self._contacts, key=lambda c: c.last_modified, reverse=True)
        else:
            raise ValueError("Unsupported sort key. Use 'name' or 'updated'.")

    def get_upcoming_birthdays(self, days: int = 7) -> List[Contact]:
        """Returns contacts with birthdays occurring within the next `days` days.

        Args:
            days (int): Number of days to look ahead. Defaults to 7.

        Returns:
            List[Contact]: A list of contacts with upcoming birthdays.
        """
        today = date.today()
        upcoming = []
        for contact in self._contacts:
            if contact.birthday:
                try:
                    bday_this_year = contact.birthday.replace(year=today.year)
                except ValueError:
                    continue  # skip invalid dates like Feb 29 on non-leap years
                delta = (bday_this_year - today).days
                if 0 <= delta <= days:
                    upcoming.append(contact)
        return upcoming
