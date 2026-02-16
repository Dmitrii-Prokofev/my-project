import json


def test_create_note_and_fetch(api_request):
    status, data = api_request(
        "POST",
        "/notes",
        {"title": "Первая", "content": "Тестовая заметка"},
    )
    assert status == 201
    created = json.loads(data)
    assert created["id"] > 0

    status, data = api_request("GET", "/notes")
    assert status == 200
    notes = json.loads(data)
    assert any(note["id"] == created["id"] for note in notes)
