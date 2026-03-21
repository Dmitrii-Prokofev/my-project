from api.delete_notes import delete_note


def test_delete_note(created_note_id):
    status, _ = delete_note(created_note_id)
    assert status == 204

    status, _ = delete_note(created_note_id)
    assert status == 404
