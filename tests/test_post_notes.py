from api.base_api import send_raw_request
from api.get_notes import get_notes
from api.post_notes import post_note


def test_create_note_success(created_note_id):
    status, notes = get_notes()
    created_note = next(note for note in notes if note["id"] == created_note_id)

    assert status == 200
    assert created_note["title"] == "Новая заметка"
    assert created_note["content"] == "Текст заметки"


def test_create_note_requires_title_and_content(api_server):
    status, data = post_note("", "Есть контент")

    assert status == 400
    assert "required" in data["detail"].lower()


def test_create_note_invalid_json(api_server):
    status, raw_data = send_raw_request("POST", "/notes", "{invalid-json")

    assert status == 400
    assert "invalid json" in raw_data.lower()
