from api.post_registration import post_registration


def test_user_registration(api_server):
    status, data = post_registration("user", "password")

    assert status == 404
    assert data["detail"].lower() == "not found"
