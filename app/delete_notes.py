from api.base_api import send_request


def delete_note(note_id: int):
    status, raw_data = send_request("DELETE", f"/notes/{note_id}")
    return status, raw_data
