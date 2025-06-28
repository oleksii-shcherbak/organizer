import pytest
from datetime import datetime
from organizer.models.note import Note


def test_note_creation():
    note = Note(title="Buy Milk", text="Remember to buy milk.", tags=["shopping"])
    assert note.title == "Buy Milk"
    assert "shopping" in note.tags
    assert isinstance(note.last_modified, datetime)


def test_note_empty_title_raises():
    with pytest.raises(ValueError):
        Note(title="", text="Some text")
