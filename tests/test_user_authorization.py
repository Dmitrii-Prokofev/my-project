class TestUserRegistration:
    def test_user_registration(self, post_registration):
        status, data = post_registration.post_registration("user", "password")

        assert status == 404
        assert data["detail"].lower() == "not found"
