from api.post_authorization import post_authorization


def test_user_authorization(api_server):
    status, data = post_authorization("user", "password")

    assert status == 404
    assert data["detail"].lower() == "not found"
