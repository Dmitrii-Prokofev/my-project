class TestPostNotes:
    def test_create_note_success(self, created_note_id, get_notes):
        status, notes = get_notes.get_notes()
        created_note = next(note for note in notes if note["id"] == created_note_id)

        assert status == 200
        assert created_note["title"] == "Новая заметка"
        assert created_note["content"] == "Текст заметки"

    def test_create_note_requires_title_and_content(self, post_notes):
        status, data = post_notes.create_note("", "Есть контент")

        assert status == 400
        assert "required" in data["detail"].lower()

    def test_create_note_invalid_json(self, post_notes):
        status, raw_data = post_notes.create_note_with_invalid_json()

        assert status == 400
        assert "invalid json" in raw_data.lower()
