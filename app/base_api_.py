import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen


class BaseApi:
    base_url = "http://localhost:8000"

    def __init__(self, token: str = ""):
        self.token = token

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _url(self, path: str):
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self.base_url}{path}"

    def send_request(self, method: str, path: str, body: dict | None = None):
        payload = None if body is None else json.dumps(body).encode("utf-8")
        request = Request(self._url(path), data=payload, headers=self._headers(), method=method)
        try:
            with urlopen(request) as response:
                return response.status, response.read().decode("utf-8")
        except HTTPError as error:
            return error.code, error.read().decode("utf-8")

    def send_raw_request(self, method: str, path: str, raw_body: str):
        request = Request(
            self._url(path),
            data=raw_body.encode("utf-8"),
            headers=self._headers(),
            method=method,
        )
        try:
            with urlopen(request) as response:
                return response.status, response.read().decode("utf-8")
        except HTTPError as error:
            return error.code, error.read().decode("utf-8")
