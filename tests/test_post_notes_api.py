import json


def test_create_note_success(api_request):
    status, data = api_request(
        "POST",
        "/notes",
        {"title": "Новая заметка", "content": "Текст заметки"},
    )

    assert status == 201
    payload = json.loads(data)
    assert payload["id"] > 0
    assert payload["title"] == "Новая заметка"
    assert payload["content"] == "Текст заметки"


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
