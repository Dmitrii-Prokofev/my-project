import threading
import time

import pytest

from api.base_api import BaseApi
from api.delete_notes import DeleteNotes
from api.get_notes import GetNotes
from api.post_notes import PostNotes
from api.post_authorization import PostAuthorization
from api.post_registration import PostRegistration
from api.models import NoteRepository, NoteService
from api.notes_api import NotesHandler, create_server


@pytest.fixture(scope="session", autouse=True)
def api_server():
    NotesHandler.service = NoteService(NoteRepository())
    BaseApi.base_url = "http://localhost:8000"

    server = create_server()
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    time.sleep(0.1)

    yield

    server.shutdown()
    server.server_close()
    thread.join()


@pytest.fixture
def get_notes(api_server):
    return GetNotes()


@pytest.fixture
def post_notes(api_server):
    return PostNotes()


@pytest.fixture
def delete_notes(api_server):
    return DeleteNotes()


@pytest.fixture
def post_authorization(api_server):
    return PostAuthorization()


@pytest.fixture
def post_registration(api_server):
    return PostRegistration()


@pytest.fixture(autouse=True)
def clean_notes(get_notes, delete_notes):
    status, notes = get_notes.get_notes()
    if status == 200:
        for note in notes:
            delete_notes.delete_note(note["id"])

    yield

    status, notes = get_notes.get_notes()
    if status == 200:
        for note in notes:
            delete_notes.delete_note(note["id"])


@pytest.fixture
def created_note_id(post_notes):
    status, data = post_notes.create_note("Новая заметка", "Текст заметки")
    assert status == 201
    return data["id"]
