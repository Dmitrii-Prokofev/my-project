from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Tuple

from app.models import NoteService


class NotesHandler(BaseHTTPRequestHandler):
    service = NoteService()

    def _send_json(self, status: int, body: dict | list) -> None:
        payload = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/notes":
            self._send_json(HTTPStatus.OK, self.service.get_notes())
            return

        if self.path.startswith("/apidocs"):
            self._send_json(
                HTTPStatus.OK,
                {
                    "title": "Notes API",
                    "methods": {
                        "GET /notes": "Get all notes",
                        "POST /notes": "Create a note",
                        "DELETE /notes/<id>": "Delete note by id",
                    },
                },
            )
            return

        self._send_json(HTTPStatus.NOT_FOUND, {"detail": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/notes":
            self._send_json(HTTPStatus.NOT_FOUND, {"detail": "Not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0

        raw = self.rfile.read(length) if length > 0 else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json(HTTPStatus.BAD_REQUEST, {"detail": "Invalid JSON"})
            return

        created = self.service.add_note(payload)
        if created is None:
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {"detail": "Fields 'title' and 'content' are required"},
            )
            return

        self._send_json(HTTPStatus.CREATED, created)

    def do_DELETE(self) -> None:  # noqa: N802
        prefix = "/notes/"
        if not self.path.startswith(prefix):
            self._send_json(HTTPStatus.NOT_FOUND, {"detail": "Not found"})
            return

        note_id_raw = self.path[len(prefix) :]
        if not note_id_raw.isdigit():
            self._send_json(HTTPStatus.BAD_REQUEST, {"detail": "note id must be integer"})
            return

        note_id = int(note_id_raw)
        if self.service.remove_note(note_id):
            self.send_response(HTTPStatus.NO_CONTENT)
            self.end_headers()
            return

        self._send_json(HTTPStatus.NOT_FOUND, {"detail": f"Note with id={note_id} not found"})


def create_server(host: str = "0.0.0.0", port: int = 8000) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), NotesHandler)


def run(host: str = "0.0.0.0", port: int = 8000) -> None:
    server = create_server(host=host, port=port)
    print(f"API started at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
