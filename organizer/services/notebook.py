from typing import List
from organizer.models.note import Note


class Notebook:
    def __init__(self) -> None:
        self._notes: List[Note] = []

    def add(self, note: Note) -> None:
        self._notes.append(note)

    def delete(self, title: str) -> bool:
        for i, note in enumerate(self._notes):
            if note.title == title:
                del self._notes[i]
                return True
        return False

    def edit(self, title: str, updated: Note) -> bool:
        for i, note in enumerate(self._notes):
            if note.title == title:
                self._notes[i] = updated
                return True
        return False

    def search(self, query: str) -> List[Note]:
        results = []
        query_lower = query.lower()
        for note in self._notes:
            combined = f"{note.title} {note.content or ''} {' '.join(note.tags)}"
            if query_lower in combined.lower():
                results.append(note)
        return results

    def all(self) -> List[Note]:
        return self._notes
