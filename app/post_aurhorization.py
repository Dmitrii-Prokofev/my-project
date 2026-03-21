import json

from api.base_api import send_request


def post_authorization(login: str, password: str):
    status, raw_data = send_request(
        "POST",
        "/authorization",
        {"login": login, "password": password},
    )
    if raw_data:
        return status, json.loads(raw_data)
    return status, None
