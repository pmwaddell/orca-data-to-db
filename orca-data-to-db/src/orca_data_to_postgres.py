import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine


def main():
    print('This script will attempt to concatenate all .csv files in the '
          'current directory into a single table in PostgreSQL.')
    engine = create_engine('postgresql://root:root@localhost:5431/orca_data')
    print('Name of the SQL table which will contain the data (press ENTER '
          'to use the default name, "q" to quit): ', end='')
    table_name = input()
    if table_name == 'q':
        print()
        quit()
    # If the user just hits enter, use default name:
    if table_name == '':
        table_name = 'orca'

    while True:
        print('Enter the value of if_exists for DataFrame.to_sql (i.e., '
              '"fail", "replace", or "append"; press ENTER to use "replace", '
              '"q" to quit): ', end='')
        if_exists = input()
        if if_exists == 'q':
            print()
            quit()
        # If the user just hits enter, replace:
        if if_exists == '':
            if_exists = 'replace'
        if if_exists not in ['fail', 'replace', 'append']:
            print(f'Invalid value for if_exists: {if_exists}')
            continue
        break

    df = pd.DataFrame()
    for f in os.listdir(os.getcwd()):
        if os.path.isfile(f):
            try:
                filename_end = f[-4:]
            except IndexError:
                # Since it is hard for filenames to be shorter than 4 chars
                # I think it is unlikely this error would ever be raised...
                print(f'{f}: Invalid filename')
                continue
            if filename_end == '.csv':
                # TODO: add logical error handling?
                new_df = pd.read_csv(f)
                df = pd.concat(objs=[df, new_df])

    df.to_sql(name=table_name, con=engine, if_exists=if_exists)
    print('Process complete!\n')


if __name__ == '__main__':
    main()
