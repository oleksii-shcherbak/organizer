import json
from pathlib import Path
from datetime import datetime, date
from typing import Any

from organizer.services.addressbook import AddressBook
from organizer.services.notebook import Notebook
from organizer.models.contact import Contact
from organizer.models.note import Note
from organizer.utils.exceptions import OrganizerError


class JSONStorage:
    """Handles saving and loading AddressBook and Notebook data to/from JSON files.

    Automatically loads existing data during initialization.
    """

    def __init__(self, base_dir: str = "data"):
        """Initializes the storage paths and loads any existing AddressBook and Notebook data.

        Args:
            base_dir (str): Directory where JSON files will be saved and loaded from.
        """
        self.base_path = Path(base_dir)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.contacts_path = self.base_path / "contacts.json"
        self.notes_path = self.base_path / "notes.json"

        # Automatically load if data exists, else create empty structures
        self.addressbook = self.load_addressbook()
        self.notebook = self.load_notebook()

    def save_addressbook(self, addressbook: AddressBook) -> None:
        """Serializes and saves the AddressBook to a JSON file.

        Args:
            addressbook (AddressBook): The address book to save.
        """
        data = [self._contact_to_dict(contact) for contact in addressbook.all()]
        self._save_to_file(self.contacts_path, data)

    def load_addressbook(self) -> AddressBook:
        """Loads the AddressBook from a JSON file.

        Returns:
            AddressBook: The loaded address book. If no file exists, returns an empty instance.
        """
        addressbook = AddressBook()
        if self.contacts_path.exists():
            data = self._load_from_file(self.contacts_path)
            for entry in data:
                contact = self._dict_to_contact(entry)
                addressbook.add(contact)
        return addressbook

    def save_notebook(self, notebook: Notebook) -> None:
        """Serializes and saves the Notebook to a JSON file.

        Args:
            notebook (Notebook): The notebook to save.
        """
        data = [self._note_to_dict(note) for note in notebook.all()]
        self._save_to_file(self.notes_path, data)

    def load_notebook(self) -> Notebook:
        """Loads the Notebook from a JSON file.

        Returns:
            Notebook: The loaded notebook. If no file exists, returns an empty instance.
        """
        notebook = Notebook()
        if self.notes_path.exists():
            data = self._load_from_file(self.notes_path)
            for entry in data:
                note = self._dict_to_note(entry)
                notebook.add(note)
        return notebook

    def _save_to_file(self, path: Path, data: Any) -> None:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _load_from_file(self, path: Path) -> Any:
        """Loads data from a JSON file.

        Args:
            path (Path): The file path to load data from.

        Returns:
            Any: The deserialized JSON content.

        Raises:
            OrganizerError: If the file is not a valid JSON.
        """
        try:
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            raise OrganizerError(f"Failed to load JSON file: {e}")

    def _contact_to_dict(self, contact: Contact) -> dict:
        return {
            "name": contact.name,
            "last_name": contact.last_name,
            "company": contact.company,
            "phone": contact.phone,
            "address": contact.address,
            "birthday": contact.birthday.isoformat() if contact.birthday else None,
            "email": contact.email,
            "last_modified": contact.last_modified.isoformat(),
        }

    def _dict_to_contact(self, data: dict) -> Contact:
        """Converts dictionary data into a Contact instance.

        Args:
            data (dict): Dictionary containing contact fields.

        Returns:
            Contact: Contact object.

        Raises:
            OrganizerError: If required fields are missing or invalid.
        """
        try:
            return Contact(
                name=data["name"],
                last_name=data.get("last_name"),
                company=data.get("company"),
                phone=data.get("phone"),
                address=data.get("address"),
                birthday=date.fromisoformat(data["birthday"]) if data.get("birthday") else None,
                email=data.get("email"),
                last_modified=datetime.fromisoformat(data["last_modified"]),
            )
        except (KeyError, TypeError, ValueError) as e:
            raise OrganizerError(f"Invalid contact data: {e}")

    def _note_to_dict(self, note: Note) -> dict:
        return {
            "title": note.title,
            "text": note.text,
            "tags": note.tags,
            "last_modified": note.last_modified.isoformat(),
        }

    def _dict_to_note(self, data: dict) -> Note:
        """Converts dictionary data into a Note instance.

        Args:
            data (dict): Dictionary containing note fields.

        Returns:
            Note: Note object.

        Raises:
            OrganizerError: If required fields are missing or invalid.
        """
        try:
            note = Note(
                title=data["title"],
                text=data.get("text"),
                tags=data.get("tags", [])
            )
            note.last_modified = datetime.fromisoformat(data["last_modified"])
            return note
        except (KeyError, TypeError, ValueError) as e:
            raise OrganizerError(f"Invalid note data: {e}")
