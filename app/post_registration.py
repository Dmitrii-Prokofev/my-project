import json

from api.base_api import BaseApi


class PostRegistration(BaseApi):
    def post_registration(self, login: str, password: str):
        status, raw_data = self.send_request(
            "POST",
            "/registration",
            {"login": login, "password": password},
        )
        if raw_data:
            return status, json.loads(raw_data)
        return status, None
