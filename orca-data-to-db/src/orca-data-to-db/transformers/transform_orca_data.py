if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # drop "Unnamed: 0"
    data = data.drop(columns='Unnamed: 0')
    # drop any columns which contain only null values
    data = data.dropna(axis=1, how='all')
    # replace "." in column names with "_", since BQ doesn't like periods
    data.columns = (data.columns.str.replace('.', '_'))
    # replace "," in column names with "_"
    data.columns = (data.columns.str.replace(',', '_'))
    # remove parens in column names
    data.columns = (data.columns.str.replace('(', ''))
    data.columns = (data.columns.str.replace(')', ''))
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
