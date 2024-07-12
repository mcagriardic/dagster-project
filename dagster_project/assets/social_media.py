from enum import StrEnum

import pandas as pd
import pandera as pa
from dagster import AssetExecutionContext, Out, graph_asset, op
from dagster_pandera import pandera_schema_to_dagster_type
from pandera.typing import Series

from dagster_project.resources.social_media_api import SocialMediaApi
from dagster_project.utils import head_md


class SocialMedia(pa.DataFrameModel):
    userId: Series[int] = pa.Field(gt=0)
    albumId: Series[int] = pa.Field(gt=0)
    postId: Series[int] = pa.Field(gt=0)
    title_posts: Series[str] = pa.Field()
    body_posts: Series[str] = pa.Field()
    title_photos: Series[str] = pa.Field()
    url: Series[str] = pa.Field()
    thumbnailUrl: Series[str] = pa.Field()
    name: Series[str] = pa.Field()
    email: Series[str] = pa.Field()
    body_comments: Series[str] = pa.Field()


SocialMediaDgType = pandera_schema_to_dagster_type(SocialMedia)


class ApiPath(StrEnum):
    # fmt: off
    POSTS    = "posts"
    PHOTOS   = "photos"
    COMMENTS = "comments"
    # fmt: on


@op
def get_posts(social_media_api: SocialMediaApi) -> pd.DataFrame:
    return social_media_api.get(ApiPath.POSTS)


@op
def get_photos(social_media_api: SocialMediaApi) -> pd.DataFrame:
    return social_media_api.get(ApiPath.PHOTOS)


@op
def get_comments(social_media_api: SocialMediaApi) -> pd.DataFrame:
    return social_media_api.get(ApiPath.COMMENTS)


@op(out=Out(io_manager_key="csv_io_manager", dagster_type=SocialMediaDgType))
def merge_dataframes(
    context: AssetExecutionContext,
    posts: pd.DataFrame,
    photos: pd.DataFrame,
    comments: pd.DataFrame,
) -> pd.DataFrame:
    metadata = {
        "posts": head_md(posts),
        "photos": head_md(photos),
        "comments": head_md(comments),
    }
    context.add_output_metadata(metadata)

    return (
        posts.merge(
            photos, left_on="userId", right_on="albumId", suffixes=("_posts", "_photos")
        )
        .merge(
            comments,
            left_on="userId",
            right_on="postId",
            suffixes=["_posts", "_comments"],
        )
        .loc[:, lambda x: ~x.columns.str.startswith("id")]
    )


@graph_asset
def transform() -> pd.DataFrame:
    return merge_dataframes(get_posts(), get_photos(), get_comments())
