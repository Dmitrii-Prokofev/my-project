from __future__ import annotations

import json
from http.client import HTTPConnection
from typing import Any


class NotesApiClient:
    """Simple API client for manual integration checks."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8000, timeout: int = 5) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout

    def _request(self, method: str, path: str, body: dict[str, Any] | None = None) -> tuple[int, Any]:
        conn = HTTPConnection(self.host, self.port, timeout=self.timeout)
        payload = json.dumps(body) if body is not None else None
        headers = {"Content-Type": "application/json"}
        conn.request(method, path, body=payload, headers=headers)
        response = conn.getresponse()
        raw_data = response.read().decode("utf-8")
        conn.close()

        if not raw_data:
            return response.status, None

        return response.status, json.loads(raw_data)

    def get_notes(self) -> tuple[int, Any]:
        return self._request("GET", "/notes")

    def create_note(self, title: str, content: str) -> tuple[int, Any]:
        return self._request("POST", "/notes", {"title": title, "content": content})

    def delete_note(self, note_id: int) -> tuple[int, Any]:
        return self._request("DELETE", f"/notes/{note_id}")
