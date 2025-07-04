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
from unittest.mock import MagicMock
import json
from pathlib import Path
from datetime import timedelta
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


def test_edit_contact(storage):
    ab = AddressBook()
    contact = Contact(name="John", phone="+123")
    ab.add(contact)

    ab.edit("John", {"phone": "+999", "email": "john@example.com"})

    edited = ab.search("John")[0]
    assert edited.phone == "+999"
    assert edited.email == "john@example.com"

def test_delete_contact(storage):
    ab = AddressBook()
    ab.add(Contact(name="Jane"))
    ab.delete("Jane")

    results = ab.search("Jane")
    assert results == []

def test_search_contact_partial(storage):
    ab = AddressBook()
    ab.add(Contact(name="Michael Johnson", email="mj@example.com"))
    ab.add(Contact(name="Michelle", phone="+456"))

    results = ab.search("Mich")
    assert len(results) == 2
    assert any("Michael" in c.name for c in results)
    assert any("Michelle" in c.name for c in results)


def test_edit_note():
    nb = Notebook()
    note = Note(title="Original Title", text="Some text", tags=["old"])
    nb.add(note)
    old_modified = note.last_modified

    nb.edit("Original Title", {"tags": ["updated", "new"]})

    assert nb.notes[0].title == "Original Title"
    assert nb.notes[0].text == "Some text"
    assert nb.notes[0].tags == ["updated", "new"]
    assert nb.notes[0].last_modified > old_modified


def test_delete_note():
    nb = Notebook()
    note = Note(title="Temporary", text="To be deleted")
    nb.add(note)

    nb.delete("Temporary")
    results = nb.search("Temporary")
    assert results == []


def test_search_note_partial_match():
    nb = Notebook()
    nb.add(Note(title="Meeting Notes", text="Discuss project roadmap", tags=["work"]))
    nb.add(Note(title="Shopping List", text="Buy milk, eggs, and bread"))

    results = nb.search("roadmap")
    assert len(results) == 1
    assert "project" in results[0].text

    results = nb.search("Shop")
    assert len(results) == 1
    assert results[0].title == "Shopping List"


def test_sort_notes_by_title():
    nb = Notebook()
    nb.add(Note(title="Bravo", text="..."))
    nb.add(Note(title="alpha", text="..."))
    nb.add(Note(title="Charlie", text="..."))

    sorted_notes = nb.sorted(by="title")
    titles = [note.title for note in sorted_notes]

    assert titles == ["alpha", "Bravo", "Charlie"]


def test_sort_notes_by_last_modified():
    nb = Notebook()
    note1 = Note(title="Note1", text="Oldest")
    note2 = Note(title="Note2", text="Middle")
    note3 = Note(title="Note3", text="Latest")

    nb.add(note1)
    nb.add(note2)
    nb.add(note3)

    note3.text = "Updated"
    note3.update_modified_time()

    note2.text = "Also updated"
    note2.update_modified_time()

    sorted_notes = nb.sorted(by="last_modified")
    titles = [note.title for note in sorted_notes]

    assert titles == ["Note2", "Note3", "Note1"]


def test_sort_notes_invalid_key_should_raise():
    nb = Notebook()
    nb.add(Note(title="One"))
    with pytest.raises(ValueError):
        nb.sorted(by="unknown_key")


def test_add_triggers_save_callback():
    mock_save = MagicMock()
    ab = AddressBook(save_callback=mock_save)
    ab.add(Contact(name="Test"))

    mock_save.assert_called_once()


def test_edit_triggers_save_callback():
    mock_save = MagicMock()
    ab = AddressBook(save_callback=mock_save)
    ab.add(Contact(name="Test", phone="+123"))
    mock_save.reset_mock()

    ab.edit("Test", {"phone": "+456"})
    mock_save.assert_called_once()


def test_delete_triggers_save_callback():
    mock_save = MagicMock()
    ab = AddressBook(save_callback=mock_save)
    ab.add(Contact(name="Test"))
    mock_save.reset_mock()

    ab.delete("Test")
    mock_save.assert_called_once()


def test_contact_last_modified_preserved(storage):
    ab = AddressBook()
    contact = Contact(name="Preserved")
    original_time = contact.last_modified
    ab.add(contact)

    storage.save_addressbook(ab)
    reloaded_ab = storage.load_addressbook()
    loaded_contact = reloaded_ab.search("Preserved")[0]

    delta = abs(loaded_contact.last_modified - original_time)
    assert delta < timedelta(milliseconds=1)


def test_note_last_modified_preserved(storage):
    nb = Notebook()
    note = Note(title="Persistent", text="Track me")
    original_time = note.last_modified
    nb.add(note)

    storage.save_notebook(nb)
    reloaded_nb = storage.load_notebook()
    loaded_note = reloaded_nb.search("Persistent")[0]

    assert loaded_note.last_modified == original_time


def test_json_file_updated_after_edit(storage):
    ab = AddressBook()
    contact = Contact(name="Track", phone="+111")
    ab.add(contact)

    storage.save_addressbook(ab)
    original_json = storage.contacts_path.read_text()

    # Edit the contact and save again
    contact.phone = "+999"
    ab.edit("Track", {"phone": "+999"})
    storage.save_addressbook(ab)

    updated_json = storage.contacts_path.read_text()
    assert original_json != updated_json
