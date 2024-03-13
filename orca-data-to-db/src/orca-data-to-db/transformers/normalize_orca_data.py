import re
import pandas as pd


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
    nested_data_sections = [
        'initial_geometry',
        'final_geometry',
        'bond_lengths',
        'bond_angles',
        'polarizability',
        'dipole_moments',
        'homo_lumo_energies',
        'mulliken_charges',
        'mulliken_charge_sums',
        'loewdin_charges',
        'loewdin_charge_sums'
    ]
    
    orca_files = pd.DataFrame()
    orca_files.insert(loc=0, column='script_input_filename', value=data['script_input_filename'])
    orca_files.insert(loc=0, column='orca_out_filename', value=data['orca_out_filename'])
    dfs_from_normalization = {
        'orca_files': orca_files
    }

    section_data_to_add = {}
    for column in data.columns:
        for section in nested_data_sections:
            regex = re.compile(fr'(' + section + ')(.*)')
            try:
                result = regex.search(column)
                # an additional 'axis' column is needed for geometry data (for x, y, z)
                if section == 'initial_geometry' or section == 'final_geometry':
                    param = result.group(2)[1:-2]    # don't include the underscore between section name and subsection
                    axis = result.group(2)[-1:]
                    rows_of_data_to_add = []
                    for index, row in data.iterrows():
                        rows_of_data_to_add.append([
                            row['orca_out_filename'],
                            param,
                            axis,
                            row[section + '_' + param + '_' + axis]
                        ])
                else:
                    param = result.group(2)[1:]    # don't include the underscore between section name and subsection
                    rows_of_data_to_add = []
                    for index, row in data.iterrows():
                        rows_of_data_to_add.append([
                            row['orca_out_filename'],
                            param,
                            row[section + '_' + param]
                        ])

                if section not in section_data_to_add.keys():
                    section_data_to_add[section] = []            
                for row in rows_of_data_to_add:
                    section_data_to_add[section].append(row)
            except AttributeError:
                continue
            break

    for section in nested_data_sections:
        # an additional 'axis' column is needed for geometry data (for x, y, z)
        if section == 'initial_geometry' or section == 'final_geometry':
                section_df = pd.DataFrame(
                section_data_to_add[section],
                columns=['orca_out_filename', section + '_parameter', 'axis', 'value']
            )
        else:
            section_df = pd.DataFrame(
                section_data_to_add[section],
                columns=['orca_out_filename', section + '_parameter', 'value']
            )
        # drop any rows with null values
        section_df.dropna(axis=0, inplace=True)
        dfs_from_normalization[section] = section_df

    return dfs_from_normalization


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
