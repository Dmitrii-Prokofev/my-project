class TestUserAuthorization:
    def test_user_authorization(self, post_authorization):
        status, data = post_authorization.post_authorization("user", "password")

        assert status == 404
        assert data["detail"].lower() == "not found"
