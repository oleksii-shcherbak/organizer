# organizer/main.py

import sys
from organizer.storage.json_storage import JSONStorage
from organizer.services.addressbook import AddressBook
from organizer.services.notebook import Notebook
from organizer.ui.app import OrganizerApp
from organizer.utils.exceptions import OrganizerError


def main():
    """
    Entry point of the Organizer application.
    Loads data and launches the Textual UI.
    """
    storage = JSONStorage("data")

    try:
        addressbook = storage.load_addressbook()
    except OrganizerError as e:
        print(f"[ERROR] Failed to load address book: {e}")
        addressbook = AddressBook()

    try:
        notebook = storage.load_notebook()
    except OrganizerError as e:
        print(f"[ERROR] Failed to load notebook: {e}")
        notebook = Notebook()

    try:
        app = OrganizerApp(addressbook=addressbook, notebook=notebook)
        app.run()
    except Exception as e:
        print(f"[FATAL] Unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
