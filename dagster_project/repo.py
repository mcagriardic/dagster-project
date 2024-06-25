from dagster import Definitions, load_assets_from_modules

from dagster_project.assets import test_asset
from dagster_project.resources.movies_api import MoviesApi

test_asset = load_assets_from_modules([test_asset])

defs = Definitions(assets=test_asset, resources={"movies_api": MoviesApi()})
