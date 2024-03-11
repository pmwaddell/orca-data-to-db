from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(dfs: dict, **kwargs) -> None:
    """
    Template for exporting data to a BigQuery warehouse.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#bigquery
    """
    dataset_export = kwargs.get('dataset_export')
    table_name_prefix_export = kwargs.get('table_name_prefix_export')
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    for table_name in dfs.keys():
        table_id = f'orca-416402.{dataset_export}.{table_name_prefix_export}_{table_name}'
        df = dfs[table_name]
        BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
            df,
            table_id,
            if_exists='replace',  # Specify resolution policy if table name already exists
        )
