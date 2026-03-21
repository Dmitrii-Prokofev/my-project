import json

from api.base_api import send_request


def get_notes():
    status, raw_data = send_request("GET", "/notes")
    return status, json.loads(raw_data)
