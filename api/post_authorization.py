import json

from api.base_api import BaseApi


class PostAuthorization(BaseApi):
    def post_authorization(self, login: str, password: str):
        status, raw_data = self.send_request(
            "POST",
            "/authorization",
            {"login": login, "password": password},
        )
        if raw_data:
            return status, json.loads(raw_data)
        return status, None
