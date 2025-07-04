# organizer/ui/app.py

from textual.app import App
from textual.widgets import Header, Footer


class OrganizerApp(App):
    """Main Textual application class for the Organizer."""

    CSS_PATH = None  # можно будет заменить на "styles.css"

    def __init__(self, addressbook, notebook, **kwargs):
        """
        Initialize the OrganizerApp with AddressBook and Notebook.

        Args:
            addressbook (AddressBook): The user's contacts.
            notebook (Notebook): The user's notes.
        """
        super().__init__(**kwargs)
        self.addressbook = addressbook
        self.notebook = notebook

    def compose(self):
        """
        Define the layout of the application UI.

        Yields:
            Widget: Header and Footer.
        """
        yield Header()
        yield Footer()
