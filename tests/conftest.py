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
