from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(dfs, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here
    schema_name = kwargs.get('schema_name_export')  # Specify the name of the schema to export data to
    table_name_prefix = kwargs.get('table_name_prefix_export')  # Specify the name of the table to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    for table_name in dfs.keys():
        df = dfs[table_name]
        with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
            loader.export(
                df,
                schema_name,
                table_name_prefix + '_' + table_name,
                index=False,  # Specifies whether to include index in exported table
                if_exists='replace',  # Specify resolution policy if table name already exists
            )
