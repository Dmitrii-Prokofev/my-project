def test_delete_note(delete_note, setup_create_note):
    status = delete_note(setup_create_note)
    assert status == 204
    status = delete_note(setup_create_note)
    assert status == 404

