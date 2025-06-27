from datetime import datetime
from typing import List, Optional


class Note:
    def __init__(self, title: str, content: Optional[str] = "", tags: Optional[List[str]] = None):
        if not title.strip():
            raise ValueError("Note title cannot be empty.")

        self.title = title.strip()
        self.content = content or ""
        self.tags = tags or []
        self.last_modified = datetime.now()

    def update(self, title: Optional[str] = None, content: Optional[str] = None, tags: Optional[List[str]] = None):
        if title is not None:
            if not title.strip():
                raise ValueError("Note title cannot be empty.")
            self.title = title.strip()
        if content is not None:
            self.content = content
        if tags is not None:
            self.tags = tags
        self.last_modified = datetime.now()

    def __repr__(self):
        return f"Note(title={self.title!r}, tags={self.tags!r}, last_modified={self.last_modified.isoformat()})"
