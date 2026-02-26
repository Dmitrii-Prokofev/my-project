import json
import threading
import time
from http.client import HTTPConnection

import pytest

from app.models import NoteRepository, NoteService
from app.notes_api import NotesHandler, create_server


@pytest.fixture(scope="module")
def api_server():
    NotesHandler.service = NoteService(NoteRepository())
    server = create_server(host="127.0.0.1", port=0)
    port = server.server_address[1]

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.05)

    yield port

    server.shutdown()
    server.server_close()
    thread.join(timeout=1)


@pytest.fixture
def api_request(api_server):
    def _request(method: str, path: str, body: dict | None = None):
        conn = HTTPConnection("127.0.0.1", api_server, timeout=3)
        headers = {"Content-Type": "application/json"}
        payload = json.dumps(body) if body is not None else None
        conn.request(method, path, body=payload, headers=headers)
        response = conn.getresponse()
        raw_data = response.read().decode("utf-8")
        conn.close()
        return response.status, raw_data

    return _request

@pytest.fixture
def get_notes(api_request):
    def _get_notes() -> list[dict]:
        status, data = api_request("GET", "/notes")
        assert status == 200
        return json.loads(data)

    return _get_notes


@pytest.fixture
def create_note(api_request):
    def _create_note(title: str = "Тестовая заметка", content: str = "Тестовый контент") -> dict:
        status, data = api_request("POST", "/notes", {"title": title, "content": content})
        assert status == 201
        return json.loads(data)

    return _create_note


@pytest.fixture
def delete_note(api_request):
    def _delete_note(note_id: int) -> int:
        status, _ = api_request("DELETE", f"/notes/{note_id}")
        return status

    return _delete_note


@pytest.fixture
def get_note_id_by_title(get_notes):
    def _get_note_id_by_title(title: str) -> int | None:
        for note in get_notes():
            if note["title"] == title:
                return note["id"]
        return None

    return _get_note_id_by_title


@pytest.fixture
def setup_create_note(create_note):
    created_note = create_note(title="Новая заметка", content="Текст заметки")
    return created_note["id"]


@pytest.fixture
def setup_teardown_note(delete_note, setup_create_note):
    yield setup_create_note
    delete_note(setup_create_note)


@pytest.fixture(autouse=True)
def clean_notes(get_notes, delete_note):
    def _delete_all_notes() -> None:
        for note in get_notes():
            delete_note(note["id"])

    _delete_all_notes()
    yield
    _delete_all_notes()