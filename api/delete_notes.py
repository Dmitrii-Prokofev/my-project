from api.base_api import BaseApi


class DeleteNotes(BaseApi):
    def delete_note(self, note_id: int):
        return self.send_request("DELETE", f"/notes/{note_id}")
