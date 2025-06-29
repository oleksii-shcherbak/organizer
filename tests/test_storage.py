"""Tests for the JSONStorage class.

This module contains unit tests for the JSONStorage class, covering:

- Exporting and importing AddressBook and Notebook data
- Handling empty datasets during export/import
- Validating error handling for invalid JSON format
- Ensuring exceptions are raised for missing required fields
- Handling invalid date formats (e.g., incorrect birthday values)
"""

import tempfile
import pytest
import json
from pathlib import Path
from organizer.models.contact import Contact
from organizer.models.note import Note
from organizer.services.addressbook import AddressBook
from organizer.services.notebook import Notebook
from organizer.storage.json_storage import JSONStorage
from organizer.utils.exceptions import OrganizerError


@pytest.fixture
def temp_dir():
    """Creates a temporary directory for storage tests."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


@pytest.fixture
def storage(temp_dir):
    """Provides a JSONStorage instance with a temporary path."""
    return JSONStorage(base_dir=temp_dir)


def test_export_import_addressbook(storage):
    """Test saving and loading address book with two contacts."""
    ab = AddressBook()
    ab.add(Contact(name="Alice", phone="+123456789", email="alice@example.com"))
    ab.add(Contact(name="Bob", address="123 Street"))

    storage.save_addressbook(ab)
    imported_ab = storage.load_addressbook()

    assert isinstance(imported_ab, AddressBook)
    assert len(imported_ab.all()) == 2
    assert imported_ab.search("Alice")[0].email == "alice@example.com"


def test_export_empty_addressbook(storage):
    ab = AddressBook()
    storage.save_addressbook(ab)
    imported_ab = storage.load_addressbook()

    assert isinstance(imported_ab, AddressBook)
    assert len(imported_ab.all()) == 0


def test_export_import_notebook(storage):
    nb = Notebook()
    note1 = Note(title="Shopping", text="Buy milk", tags=["groceries"])
    note2 = Note(title="Workout", text="Leg day")
    nb.add(note1)
    nb.add(note2)

    storage.save_notebook(nb)
    imported_nb = storage.load_notebook()

    assert isinstance(imported_nb, Notebook)
    notes = imported_nb.all()
    assert len(notes) == 2
    assert notes[0].title == "Shopping"
    assert notes[1].text == "Leg day"


def test_export_empty_notebook(storage):
    nb = Notebook()
    storage.save_notebook(nb)
    imported_nb = storage.load_notebook()

    assert isinstance(imported_nb, Notebook)
    assert len(imported_nb.all()) == 0


def test_invalid_json_file_should_raise(storage, temp_dir):
    path = Path(temp_dir) / "broken.json"
    path.write_text("this is not json")

    with pytest.raises(OrganizerError):
        storage._load_from_file(path)


def test_invalid_birthday_format_should_raise(storage, temp_dir):
    path = Path(temp_dir) / "contacts.json"
    bad_data = [{
        "name": "Test",
        "last_name": None,
        "company": None,
        "phone": None,
        "address": None,
        "birthday": "2024-13-01",  # Invalid month
        "email": None,
        "last_modified": "2024-01-01T00:00:00"
    }]
    path.write_text(json.dumps(bad_data))

    with pytest.raises(OrganizerError):
        storage.load_addressbook()


def test_missing_required_contact_field_should_raise(storage, temp_dir):
    path = Path(temp_dir) / "contacts.json"
    invalid_contact = [{
        "phone": "+123456789",
        "last_modified": "2024-01-01T00:00:00"
    }]
    path.write_text(json.dumps(invalid_contact))

    with pytest.raises(OrganizerError):
        storage.load_addressbook()


def test_missing_required_note_field_should_raise(storage, temp_dir):
    path = Path(temp_dir) / "notes.json"
    invalid_note = [{
        "text": "Some text",
        "tags": [],
        "last_modified": "2024-01-01T00:00:00"
    }]
    path.write_text(json.dumps(invalid_note))

    with pytest.raises(OrganizerError):
        storage.load_notebook()
