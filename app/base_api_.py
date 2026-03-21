import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE_URL = "http://185.240.103.201:8000"
TOKEN = ""


def set_base_url(url: str):
    global BASE_URL
    BASE_URL = url


def set_token(token: str):
    global TOKEN
    TOKEN = token


def _make_url(path: str):
    if not path.startswith("/"):
        path = f"/{path}"
    return f"{BASE_URL}{path}"


def _make_headers():
    headers = {"Content-Type": "application/json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    return headers


def send_request(method: str, path: str, body: dict | None = None):
    payload = None
    if body is not None:
        payload = json.dumps(body).encode("utf-8")

    request = Request(
        url=_make_url(path),
        data=payload,
        headers=_make_headers(),
        method=method,
    )

    try:
        with urlopen(request) as response:
            return response.status, response.read().decode("utf-8")
    except HTTPError as error:
        return error.code, error.read().decode("utf-8")


def send_raw_request(method: str, path: str, raw_body: str):
    request = Request(
        url=_make_url(path),
        data=raw_body.encode("utf-8"),
        headers=_make_headers(),
        method=method,
    )

    try:
        with urlopen(request) as response:
            return response.status, response.read().decode("utf-8")
    except HTTPError as error:
        return error.code, error.read().decode("utf-8")
