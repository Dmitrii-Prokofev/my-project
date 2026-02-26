def test_get_notes_initially_empty(get_notes):
    assert get_notes() == []