from api.get_notes import get_notes


def test_get_notes(api_server):
    status, notes = get_notes()

    assert status == 200
    assert notes == []
