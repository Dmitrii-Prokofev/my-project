import json

from api.base_api import send_request


def post_note(title: str, content: str):
    status, raw_data = send_request(
        "POST",
        "/notes",
        {"title": title, "content": content},
    )
    if raw_data:
        return status, json.loads(raw_data)
    return status, None
