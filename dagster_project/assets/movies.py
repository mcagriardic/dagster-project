import pandas as pd
import pandera as pa
from dagster import AssetExecutionContext, MetadataValue, asset, get_dagster_logger
from dagster_pandera import pandera_schema_to_dagster_type
from pandera.typing import Series

from dagster_project.resources.movies_api import MoviesApi

logger = get_dagster_logger()


class Movies(pa.SchemaModel):
    id: Series[int] = pa.Field(gt=0)
    title: Series[str] = pa.Field()
    vote_average: Series[float] = pa.Field(ge=0)
    vote_count: Series[int] = pa.Field(ge=0)
    status: Series[str] = pa.Field()
    release_date: Series[pa.DateTime] = pa.Field(nullable=True)
    revenue: Series[float] = pa.Field(ge=0)
    runtime: Series[int] = pa.Field(ge=0)
    adult: Series[bool] = pa.Field()
    backdrop_path: Series[str] = pa.Field(nullable=True)
    budget: Series[int] = pa.Field(ge=0)
    homepage: Series[str] = pa.Field(nullable=True)
    imdb_id: Series[str] = pa.Field(nullable=True)
    original_language: Series[str] = pa.Field()
    original_title: Series[str] = pa.Field()
    overview: Series[str] = pa.Field(nullable=True)
    popularity: Series[float] = pa.Field(ge=0)
    poster_path: Series[str] = pa.Field(nullable=True)
    tagline: Series[str] = pa.Field(nullable=True)
    genres: Series[str] = pa.Field(nullable=True)
    production_companies: Series[str] = pa.Field(nullable=True)
    production_countries: Series[str] = pa.Field(nullable=True)
    spoken_languages: Series[str] = pa.Field(nullable=True)
    keywords: Series[str] = pa.Field(nullable=True)


MoviesDagsterType = pandera_schema_to_dagster_type(Movies)


@asset(dagster_type=MoviesDagsterType, io_manager_key="csv_io_manager")
def test_asset(context: AssetExecutionContext, movies_api: MoviesApi) -> pd.DataFrame:
    df = movies_api.get("/get_all")
    context.add_output_metadata({"preview": MetadataValue.md(df.head().to_markdown())})
    return df.assign(release_date=lambda x: pd.to_datetime(x["release_date"]))


@asset(dagster_type=MoviesDagsterType, io_manager_key="csv_io_manager")
def downstream_asset(test_asset: pd.DataFrame) -> pd.DataFrame:
    return test_asset.loc[:, ~test_asset.columns.str.contains("Unnamed")]
