from dagster import asset, get_dagster_logger
from requests import Response

from dagster_project.resources.movies_api import MoviesApi

logger = get_dagster_logger()


@asset
def test_asset(movies_api: MoviesApi) -> Response:
    response = movies_api.get("/")
    logger.info(response)
    return response
