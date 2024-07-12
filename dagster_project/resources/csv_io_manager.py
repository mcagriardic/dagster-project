from pathlib import Path
from typing import Any

import pandas as pd
from dagster import (
    InputContext,
    IOManager,
    OutputContext,
    TableSchema,
    TableSchemaMetadataValue,
    get_dagster_logger,
)

logger = get_dagster_logger()


class CsvIoManager(IOManager):
    storage_directory = Path("dagster_conf/csv_io_manager")

    def _get_fs_path(self, context: OutputContext):
        filename = (
            context.step_key
            if context.step_key == context.name
            else f"{context.step_key}-{context.name}"
        )
        return self.storage_directory / f"{filename}.csv"

    def get_schema(self, dagster_type):
        schema_value = next(
            (
                x
                for x in dagster_type.metadata.values()
                if isinstance(x, TableSchemaMetadataValue)
            ),
            None,
        )
        assert schema_value
        return schema_value.schema

    @staticmethod
    def get_column_to_type_mapping(schema: TableSchema) -> dict[str, str]:
        col_to_type = {}
        for col in schema.columns:
            col_to_type[col.name] = col.type if col.type != "int64" else "Int64"
        return col_to_type

    def load_input(self, context: InputContext) -> Any:
        upstream_context = context.upstream_output
        fs_path = self._get_fs_path(upstream_context)

        schema = self.get_schema(upstream_context.dagster_type)
        col_to_type = self.get_column_to_type_mapping(schema)

        return pd.read_csv(fs_path).astype(col_to_type)

    def handle_output(self, context: OutputContext, df: pd.DataFrame) -> None:
        fs_path = self._get_fs_path(context)
        df.to_csv(fs_path)
