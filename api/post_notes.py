import json

from api.base_api import BaseApi


class PostNotes(BaseApi):
    def create_note(self, title: str, content: str):
        status, raw_data = self.send_request(
            "POST",
            "/notes",
            {"title": title, "content": content},
        )
        if raw_data:
            return status, json.loads(raw_data)
        return status, None

    def create_note_with_invalid_json(self):
        return self.send_raw_request("POST", "/notes", "{invalid-json")
