import json
from typing import Any

import pandas as pd
import requests
from dagster import ConfigurableResource, get_dagster_logger
from requests import Response

logger = get_dagster_logger()


class SocialMediaApi(ConfigurableResource):
    api_base_url: str = "http://fastapi:8000"

    def _get_response_content(self, response: Response) -> list[dict[str, Any]]:
        return response.content.decode()

    def _response_to_dataframe(self, response: Response) -> pd.DataFrame:
        return pd.DataFrame(
            json.loads(
                self._get_response_content(response),
            ),
        )

    def get(self, endpoint: str) -> pd.DataFrame:
        response = requests.get(
            f"{self.api_base_url}/{endpoint}", headers={"user-agent": "dagster"}
        )
        if not response.ok:
            raise RuntimeError(f"Unexpected return code: {response.status_code}")
        return self._response_to_dataframe(response)
