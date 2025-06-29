import tempfile
import pytest
from organizer.models.contact import Contact
from organizer.models.note import Note
from organizer.services.addressbook import AddressBook
from organizer.services.notebook import Notebook
from organizer.storage.json_storage import JSONStorage

# ============================== Fixtures ==============================

@pytest.fixture
def temp_dir():
    """Creates a temporary directory for storage tests."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

@pytest.fixture
def storage(temp_dir):
    """Provides a JSONStorage instance with a temporary path."""
    return JSONStorage(base_dir=temp_dir)

# ============================== AddressBook Tests ==============================

def test_export_import_addressbook(storage):
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

# ============================== Notebook Tests ==============================

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
