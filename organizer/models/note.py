from datetime import datetime
from typing import List, Optional


class Note:
    def __init__(self, title: str, text: Optional[str] = "", tags: Optional[List[str]] = None):
        if not title.strip():
            raise ValueError("Note title cannot be empty.")

        self.title = title.strip()
        self.text = text or ""
        self.tags = tags or []
        self.last_modified = datetime.now()

    def update(self, title: Optional[str] = None, text: Optional[str] = None, tags: Optional[List[str]] = None):
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
        if not self.tags:
            self.tags = []
        self.tags.append(tag)
        self.last_modified = datetime.now()

    def __repr__(self):
        return f"Note(title={self.title!r}, text={self.text!r} tags={self.tags!r})"
