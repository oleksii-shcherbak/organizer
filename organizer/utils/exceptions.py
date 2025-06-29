class OrganizerError(Exception):
    """Base exception class for all custom errors in the Organizer application."""
    pass


class NoteNotFoundError(OrganizerError):
    """Raised when a note with the given title is not found.

    Attributes:
        title (str): The title of the note that was not found.
    """

    def __init__(self, title: str):
        self.title = title
        super().__init__(f"Note '{title}' not found.")


class ContactNotFoundError(OrganizerError):
    """Raised when a contact with the given name is not found.

    Attributes:
        name (str): The name of the contact that was not found.
    """

    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Contact '{name}' not found.")


class ValidationError(OrganizerError):
    """Raised when input validation fails, such as for email or phone format.

    Attributes:
        message (str): Explanation of the validation failure.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class DuplicateEntryError(OrganizerError):
    """Raised when attempting to add a duplicate entry that is not allowed.

    Attributes:
        entry_type (str): The type of entry (e.g., 'Contact', 'Note').
        identifier (str): The identifier of the duplicate entry.
    """

    def __init__(self, entry_type: str, identifier: str):
        self.entry_type = entry_type
        self.identifier = identifier
        super().__init__(f"{entry_type} '{identifier}' already exists.")
