from typing import Optional, List
from organizer.models.note import Note
from organizer.utils.exceptions import (
    NoteNotFoundError,
    ValidationError,
    DuplicateEntryError,
)


class Notebook:
    """Manages a collection of Note objects with operations like add, edit, delete, search, and sort."""

    def __init__(self) -> None:
        """Initializes an empty Notebook."""
        self._notes: List[Note] = []

    def add(self, note: Note) -> None:
        """Adds a note to the notebook.

        Args:
            note (Note): The note to add.

        Raises:
            ValidationError: If the note is None or lacks a title.
            DuplicateEntryError: If a note with the same title already exists.
        """
        if note is None:
            raise ValidationError("Note cannot be None.")
        if not note.title or not note.title.strip():
            raise ValidationError("Note title cannot be empty.")
        if any(n.title == note.title for n in self._notes):
            raise DuplicateEntryError("Duplicate note title", note.title)
        self._notes.append(note)

    def get(self, title: str) -> Optional[Note]:
        """Retrieves a note by its title.

        Args:
            title (str): The title of the note to retrieve.

        Returns:
            Note: The found note with the given title.

        Raises:
            NoteNotFoundError: If no note with the given title is found.
        """
        for note in self._notes:
            if note.title == title:
                return note
        raise NoteNotFoundError(title)

    def delete(self, title: str) -> bool:
        """Deletes the first note found with the given title.

        Args:
            title (str): The title of the note to delete.

        Returns:
            bool: True if a note was deleted.

        Raises:
            NoteNotFoundError: If no note with the given title is found.
        """
        for i, note in enumerate(self._notes):
            if note.title == title:
                del self._notes[i]
                return True
        raise NoteNotFoundError(title)

    def edit(self, title: str, updated: Note) -> bool:
        """Edits a note by replacing it with the provided updated note.

        Args:
            title (str): The title of the note to be edited.
            updated (Note): The updated note instance.

        Returns:
            bool: True if the note was successfully edited.

        Raises:
            NoteNotFoundError: If no note with the given title is found.
            ValidationError: If the updated note is None.
        """
        if updated is None:
            raise ValidationError("Cannot edit with a None note.")

        for i, note in enumerate(self._notes):
            if note.title == title:
                self._notes[i] = updated
                return True

        raise NoteNotFoundError(title)

    def search(self, query: str) -> List[Note]:
        """Searches for notes that contain the query in the title, text, or tags.

        Args:
            query (str): The query string to search for.

        Returns:
            List[Note]: A list of matching notes.
        """
        results = []
        query_lower = query.lower()
        for note in self._notes:
            combined = f"{note.title} {note.text or ''} {' '.join(note.tags)}"
            if query_lower in combined.lower():
                results.append(note)
        return results

    def all(self) -> List[Note]:
        """Returns all notes in the notebook.

        Returns:
            List[Note]: A list of all notes.
        """
        return self._notes

    def sorted(self, by: str = "title") -> List[Note]:
        """Sorts the notes by a given attribute.

        Args:
            by (str): The attribute to sort by. Options are "title" or "last_modified".

        Returns:
            List[Note]: A sorted list of notes.

        Raises:
            ValueError: If the sort key is unsupported.
        """
        if by == "title":
            return sorted(self._notes, key=lambda n: n.title.lower())
        elif by == "last_modified":
            return sorted(self._notes, key=lambda n: n.last_modified, reverse=True)
        else:
            raise ValueError("Unsupported sort key. Use 'title' or 'last_modified'.")
