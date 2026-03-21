import json

from api.base_api import BaseApi


class GetNotes(BaseApi):
    def get_notes(self):
        status, raw_data = self.send_request("GET", "/notes")
        return status, json.loads(raw_data)
