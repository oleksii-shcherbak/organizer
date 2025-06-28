from datetime import datetime
from typing import List, Optional


class Note:
    """Represents a note with a title, optional text, and tags.

    Attributes:
        title (str): The title of the note. Cannot be empty.
        text (str): The content/body of the note.
        tags (List[str]): A list of tags associated with the note.
        last_modified (datetime): Timestamp of the last modification.
    """

    def __init__(self, title: str, text: Optional[str] = "", tags: Optional[List[str]] = None):
        """Initializes a new Note instance.

        Args:
            title (str): The title of the note. Cannot be empty or whitespace.
            text (Optional[str]): The text content of the note. Defaults to an empty string.
            tags (Optional[List[str]]): Optional list of tags. Defaults to an empty list.

        Raises:
            ValueError: If the title is empty or only whitespace.
        """
        if not title.strip():
            raise ValueError("Note title cannot be empty.")

        self.title = title.strip()
        self.text = text or ""
        self.tags = tags or []
        self.last_modified = datetime.now()

    def update(self, title: Optional[str] = None, text: Optional[str] = None, tags: Optional[List[str]] = None):
        """Updates the title, text, and/or tags of the note.

        Args:
            title (Optional[str]): New title for the note. Cannot be empty if provided.
            text (Optional[str]): New text content.
            tags (Optional[List[str]]): New list of tags.

        Raises:
            ValueError: If the new title is empty or only whitespace.
        """
        if title is not None:
            if not title.strip():
                raise ValueError("Note title cannot be empty.")
            self.title = title.strip()
        if text is not None:
            self.text = text
        if tags is not None:
            self.tags = tags
        self.last_modified = datetime.now()

    def add_tag(self, tag: str) -> None:
        """Adds a tag to the note.

        Args:
            tag (str): The tag to be added.
        """
        if not self.tags:
            self.tags = []
        self.tags.append(tag)
        self.last_modified = datetime.now()

    def __repr__(self):
        """Returns a string representation of the Note object.

        Returns:
            str: A string showing the note's title, text, and tags.
        """
        return f"Note(title={self.title!r}, text={self.text!r}, tags={self.tags!r})"
