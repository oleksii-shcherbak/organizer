from typing import Optional, List
from organizer.models.contact import Contact


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
        query_lower = query.lower()
        for contact in self._contacts.values():
            combined = " ".join([
                contact.name or "",
                contact.last_name or "",
                contact.company or "",
                contact.phone or "",
                contact.address or "",
                contact.email or ""
            ])
            if query_lower in combined.lower():
                results.append(contact)
        return results

    def all(self) -> List[Contact]:
        return list(self._contacts.values())
