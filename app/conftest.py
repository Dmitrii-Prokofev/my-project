import threading
import time

import pytest

from api.base_api import set_base_url
from api.delete_notes import delete_note
from api.get_notes import get_notes
from api.post_notes import post_note
from app.models import NoteRepository, NoteService
from app.notes_api import NotesHandler, create_server


@pytest.fixture(scope="session", autouse=True)
def api_server():
    NotesHandler.service = NoteService(NoteRepository())
    set_base_url("http://localhost:8000")

    server = create_server()
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    time.sleep(0.1)

    yield

    server.shutdown()
    server.server_close()
    thread.join()


@pytest.fixture(autouse=True)
def clean_notes(api_server):
    status, notes = get_notes()
    if status == 200:
        for note in notes:
            delete_note(note["id"])

    yield


@pytest.fixture
def created_note_id(api_server):
    status, note = post_note("Новая заметка", "Текст заметки")
    assert status == 201
    return note["id"]
