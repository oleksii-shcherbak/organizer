"""Tests for the Notebook service and Note model.

This module includes a comprehensive test suite covering:

- Adding, retrieving, editing, and deleting notes
- Duplicate titles handling
- Tag manipulation and search
- Sorting by title and modification date
- Validation of note inputs (e.g., None or empty title)
- Unicode, special characters, and edge-case searches
"""

import pytest
from datetime import timedelta
from organizer.services.notebook import Notebook
from organizer.models.note import Note
from organizer.utils.exceptions import (
    NoteNotFoundError,
    ValidationError,
    DuplicateEntryError,
)


def test_notebook_add_and_get_note():
    notebook = Notebook()
    note = Note(title="Note1", text="Text")
    notebook.add(note)

    retrieved = notebook.get("Note1")
    assert retrieved is not None
    assert retrieved.title == "Note1"


def test_notebook_delete_note():
    notebook = Notebook()
    note = Note(title="Note2", text="Text")
    notebook.add(note)

    assert notebook.delete("Note2") is True

    with pytest.raises(NoteNotFoundError):
        notebook.get("Note2")


def test_notebook_search():
    notebook = Notebook()
    note1 = Note(title="Buy Milk", text="Get whole milk", tags=["groceries"])
    note2 = Note(title="Buy Bread", text="Whole grain")
    notebook.add(note1)
    notebook.add(note2)

    results = notebook.search("milk")
    assert len(results) == 1
    assert results[0].title == "Buy Milk"


def test_notebook_delete_nonexistent_note_raises():
    notebook = Notebook()
    with pytest.raises(NoteNotFoundError) as exc_info:
        notebook.delete("NonExistent")
    assert "NonExistent" in str(exc_info.value)


def test_notebook_edit_nonexistent_note_raises():
    notebook = Notebook()
    with pytest.raises(NoteNotFoundError) as exc:
        notebook.edit("NonExistent", {"text": "Changed"})
    assert "NonExistent" in str(exc.value)


def test_notebook_search_returns_empty_for_no_match():
    notebook = Notebook()
    note = Note(title="Buy Eggs", text="Organic")
    notebook.add(note)
    results = notebook.search("milk")  # no match
    assert results == []


def test_notebook_add_duplicate_title_allowed():
    notebook = Notebook()
    note1 = Note(title="Same", text="First")
    note2 = Note(title="Same", text="Second")
    notebook.add(note1)

    with pytest.raises(DuplicateEntryError):
        notebook.add(note2)


def test_note_creation_with_empty_tag_list():
    note = Note(title="Test", text="Empty tags test", tags=[])
    assert note.tags == []


def test_notebook_edit_successfully_changes_note():
    notebook = Notebook()
    note = Note(title="Plan", text="Old text", tags=["old"])
    updated = Note(title="Plan", text="Updated text", tags=["new"])
    notebook.add(note)
    result = notebook.edit("Plan", {"text": "Updated text", "tags": ["new"]})
    assert result is True
    note = notebook.all()[0]
    assert note.text == "Updated text"
    assert note.tags == ["new"]


def test_notebook_add_none_raises_exception():
    notebook = Notebook()
    with pytest.raises(ValidationError):
        notebook.add(None)


def test_notebook_edit_with_none_raises_validation_error():
    notebook = Notebook()
    notebook.add(Note(title="Note", text="Text"))
    with pytest.raises(ValidationError) as exc:
        notebook.edit("Note", None)
    assert "None" in str(exc.value)


def test_notebook_get_case_sensitive():
    notebook = Notebook()
    notebook.add(Note(title="Important", text="case test"))

    with pytest.raises(NoteNotFoundError):
        notebook.get("important")


def test_sort_by_title():
    notebook = Notebook()
    notebook.add(Note(title="B Title", text="text"))
    notebook.add(Note(title="A Title", text="text"))
    sorted_notes = notebook.sorted(by="title")
    assert [n.title for n in sorted_notes] == ["A Title", "B Title"]


def test_sort_by_last_modified():
    notebook = Notebook()
    note1 = Note(title="First", text="first")
    note2 = Note(title="Second", text="second")
    note1.last_modified -= timedelta(minutes=5)
    notebook.add(note1)
    notebook.add(note2)
    sorted_notes = notebook.sorted(by="last_modified")
    assert sorted_notes[0].title == "Second"
    assert sorted_notes[1].title == "First"


def test_search_email_inside_note_text():
    notebook = Notebook()
    notebook.add(Note(title="EmailNote", text="Please contact me at test@example.com"))
    result = notebook.search("test@example.com")
    assert len(result) == 1 and result[0].title == "EmailNote"


def test_search_phone_inside_note_text():
    notebook = Notebook()
    notebook.add(Note(title="PhoneNote", text="Call me at +380123456789"))
    result = notebook.search("+380123456789")
    assert len(result) == 1 and result[0].title == "PhoneNote"


def test_search_by_tag():
    notebook = Notebook()
    note = Note(title="TaggedNote", text="Contains tag")
    note.add_tag("urgent")
    notebook.add(note)
    result = notebook.search("urgent")
    assert len(result) == 1 and result[0].title == "TaggedNote"


def test_unicode_handling():
    notebook = Notebook()
    notebook.add(Note(title="Привіт", text="Це нотатка українською мовою"))
    notebook.add(Note(title="こんにちは", text="日本語のメモ"))
    result_ua = notebook.search("українською")
    result_jp = notebook.search("日本語")
    assert len(result_ua) == 1 and result_ua[0].title == "Привіт"
    assert len(result_jp) == 1 and result_jp[0].title == "こんにちは"


def test_search_with_spaces_and_special_chars():
    notebook = Notebook()
    notebook.add(Note(title="Special!@#Note", text="Some weird text $$$ and more"))
    result = notebook.search("$$$")
    assert len(result) == 1 and result[0].title == "Special!@#Note"


def test_note_creation_with_minimal_fields():
    note = Note(title="Minimal")
    assert note.title == "Minimal"
    assert note.text == ""
    assert note.tags is None or note.tags == []


def test_sort_with_invalid_key_raises_error():
    notebook = Notebook()
    notebook.add(Note(title="Test", text="text"))
    with pytest.raises(ValueError):
        notebook.sorted(by="unknown_key")
