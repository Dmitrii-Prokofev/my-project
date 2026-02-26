def test_create_note_success(get_notes, setup_teardown_note):
    notes = get_notes()
    created_note = next(note for note in notes if note["id"] == setup_teardown_note)
    assert created_note["title"] == "Новая заметка"
    assert created_note["content"] == "Текст заметки"

def test_create_note_requires_title_and_content(api_request):
    status, data = api_request("POST", "/notes", {"title": "", "content": "Есть контент"})
    assert status == 400
    assert "required" in data.lower()

    status, data = api_request("POST", "/notes", {"title": "Есть заголовок", "content": ""})
    assert status == 400
    assert "required" in data.lower()


def test_create_note_invalid_json(api_server):
    from http.client import HTTPConnection

    conn = HTTPConnection("127.0.0.1", api_server, timeout=3)
    conn.request(
        "POST",
        "/notes",
        body="{invalid-json",
        headers={"Content-Type": "application/json"},
    )
    response = conn.getresponse()
    raw_data = response.read().decode("utf-8")
    conn.close()

    assert response.status == 400
    assert "invalid json" in raw_data.lower()
