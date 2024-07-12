import pandas as pd
from dagster import MetadataValue


def head_md(df: pd.DataFrame) -> MetadataValue:
    return MetadataValue.md(df.head().to_markdown())
