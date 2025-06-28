from organizer.services.notebook import Notebook
from organizer.models.note import Note


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
    assert notebook.get("Note2") is None


def test_notebook_search():
    notebook = Notebook()
    note1 = Note(title="Buy Milk", text="Get whole milk", tags=["groceries"])
    note2 = Note(title="Buy Bread", text="Whole grain")
    notebook.add(note1)
    notebook.add(note2)

    results = notebook.search("milk")
    assert len(results) == 1
    assert results[0].title == "Buy Milk"
