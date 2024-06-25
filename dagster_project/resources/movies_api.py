import requests
from dagster import ConfigurableResource
from requests import Response


class MoviesApi(ConfigurableResource):
    api_base_url: str = "http://fastapi:8000"

    def get(self, endpoint: str) -> Response:
        return requests.get(
            f"{self.api_base_url}/{endpoint}", headers={"user-agent": "dagster"}
        )
