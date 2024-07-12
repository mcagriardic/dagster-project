import time
from enum import StrEnum

import pandas as pd
import pandera as pa
from dagster import AssetKey, AssetOut, Output, asset, multi_asset
from dagster_pandera import pandera_schema_to_dagster_type
from pandera.typing import Series

from dagster_project.resources.social_media_api import SocialMediaApi


class Posts(pa.SchemaModel):
    userId: Series[int] = pa.Field(gt=0)
    id: Series[int] = pa.Field(gt=0)
    body: Series[str] = pa.Field()
    title: Series[str] = pa.Field()


class Photos(pa.SchemaModel):
    albumId: Series[int] = pa.Field(gt=0)
    id: Series[int] = pa.Field(gt=0)
    title: Series[str] = pa.Field()
    url: Series[str] = pa.Field()
    thumbnailUrl: Series[str] = pa.Field()


PostsDgType = pandera_schema_to_dagster_type(Posts)
PhotosDgType = pandera_schema_to_dagster_type(Photos)


class ApiPath(StrEnum):
    # fmt: off
    POSTS    = "posts"
    PHOTOS   = "photos"
    COMMENTS = "comments"
    # fmt: on


@asset()
def a():
    return 1


@asset()
def b():
    return 1


@asset()
def c():
    return 1


@multi_asset(
    outs={
        "photos": AssetOut(
            io_manager_key="csv_io_manager",
            dagster_type=PhotosDgType,
            is_required=False,
        ),
        "posts": AssetOut(
            io_manager_key="csv_io_manager",
            dagster_type=PostsDgType,
            is_required=False,
        ),
    },
    internal_asset_deps={
        "photos": {AssetKey("a")},
        "posts": {AssetKey("a"), AssetKey("b"), AssetKey("c")},
    },
)
def photos_and_posts(
    a: int,
    b: int,
    c: int,
    social_media_api: SocialMediaApi,
) -> pd.DataFrame:
    even = int(time.time()) % 2 == 0
    # Only one will execute. Use yield with `Output`, not `return`.
    if even:
        yield Output(social_media_api.get(ApiPath.PHOTOS), output_name="photos")
    else:
        yield Output(social_media_api.get(ApiPath.POSTS), output_name="posts")
