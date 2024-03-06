import pandas as pd
import psycopg2
from sqlalchemy import create_engine


csv_name = '../data/ORCA_data_PPh3_test_input.csv'

# TODO: run on all files with .csv, concatenate w pandas I suppose
df = pd.read_csv(csv_name)
print(df.head())

engine = create_engine('postgresql://root:root@localhost:5431/orca_data')

df.to_sql(name='PPh3_test', con=engine, if_exists='replace')
