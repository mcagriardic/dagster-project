from dagster import (
    Definitions,
    FilesystemIOManager,
    define_asset_job,
    load_assets_from_modules,
)

from dagster_project.assets import movies, multi_asset, social_media
from dagster_project.resources.csv_io_manager import CsvIoManager
from dagster_project.resources.movies_api import MoviesApi
from dagster_project.resources.social_media_api import SocialMediaApi

posts_or_photos_job = define_asset_job(
    "posts_or_photos_job", selection=["posts", "photos"]
)

movies_assets = load_assets_from_modules([movies])
social_media_assets = load_assets_from_modules([social_media])
multi_asset_assets = load_assets_from_modules([multi_asset])

resources = {
    "io_manager": FilesystemIOManager(),
    "csv_io_manager": CsvIoManager(),
    "movies_api": MoviesApi(),
    "social_media_api": SocialMediaApi(),
}

defs = Definitions(
    assets=movies_assets + social_media_assets + multi_asset_assets,
    jobs=[posts_or_photos_job],
    resources=resources,
)
