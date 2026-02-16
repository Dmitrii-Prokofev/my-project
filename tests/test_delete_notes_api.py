import json


def test_delete_note(api_request):
    status, data = api_request(
        "POST",
        "/notes",
        {"title": "Удалить", "content": "Нужно удалить"},
    )
    assert status == 201
    note_id = json.loads(data)["id"]

    status, _ = api_request("DELETE", f"/notes/{note_id}")
    assert status == 204

    status, data = api_request("DELETE", f"/notes/{note_id}")
    assert status == 404
    assert "not found" in data.lower()
