from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List, Optional


@dataclass
class Note:
    id: int
    title: str
    content: str

    def to_dict(self) -> dict:
        return asdict(self)


class NoteRepository:
    """Repository layer for storing notes in memory."""

    def __init__(self) -> None:
        self._notes: Dict[int, Note] = {}
        self._next_id = 1

    def list_notes(self) -> List[Note]:
        return list(self._notes.values())

    def create_note(self, title: str, content: str) -> Note:
        note = Note(id=self._next_id, title=title, content=content)
        self._notes[self._next_id] = note
        self._next_id += 1
        return note

    def delete_note(self, note_id: int) -> bool:
        return self._notes.pop(note_id, None) is not None


class NoteService:
    """Service layer with note-related business logic."""

    def __init__(self, repository: Optional[NoteRepository] = None) -> None:
        self._repository = repository or NoteRepository()

    def get_notes(self) -> List[dict]:
        return [note.to_dict() for note in self._repository.list_notes()]

    def add_note(self, payload: dict) -> Optional[dict]:
        title = str(payload.get("title", "")).strip()
        content = str(payload.get("content", "")).strip()
        if not title or not content:
            return None

        note = self._repository.create_note(title=title, content=content)
        return note.to_dict()

    def remove_note(self, note_id: int) -> bool:
        return self._repository.delete_note(note_id)
