import json


def test_get_notes_initially_empty(api_request):
    status, data = api_request("GET", "/notes")
    assert status == 200
    assert json.loads(data) == []
