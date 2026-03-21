class TestGetNotes:
    def test_get_notes(self, get_notes):
        status, notes = get_notes.get_notes()

        assert status == 200
        assert notes == []
