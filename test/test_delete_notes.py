class TestDeleteNotes:
    def test_delete_note(self, created_note_id, delete_notes):
        status, _ = delete_notes.delete_note(created_note_id)
        assert status == 204

        status, _ = delete_notes.delete_note(created_note_id)
        assert status == 404
