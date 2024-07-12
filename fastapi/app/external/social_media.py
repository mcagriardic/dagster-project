import json
import time
from enum import StrEnum

import requests
from requests import Response


class EndPoint(StrEnum):
    POSTS = "https://jsonplaceholder.typicode.com/posts"
    PHOTOS = "https://jsonplaceholder.typicode.com/photos"
    COMMENTS = "https://jsonplaceholder.typicode.com/comments"


def get_posts() -> dict[str, str]:
    response: Response = requests.get(EndPoint.POSTS)
    time.sleep(1)
    if not response.ok:
        raise ValueError(f"Not OK response code: {response.status_code}")
    return json.loads(response.content.decode())


def get_photos() -> dict[str, str]:
    response: Response = requests.get(EndPoint.PHOTOS)
    time.sleep(5)
    if not response.ok:
        raise ValueError(f"Not OK response code: {response.status_code}")
    return json.loads(response.content.decode())


def get_comments() -> dict[str, str]:
    response: Response = requests.get(EndPoint.COMMENTS)
    time.sleep(3)
    if not response.ok:
        raise ValueError(f"Not OK response code: {response.status_code}")
    return json.loads(response.content.decode())
