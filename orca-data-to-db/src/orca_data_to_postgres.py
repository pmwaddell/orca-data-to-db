import os
import pandas as pd
from sqlalchemy import create_engine


json_name = '../data/ORCA_data_PPh3_test_input.json'
df = pd.read_json(json_name)  # not sure about index_col=False...
print(df.head())

engine = create_engine('postgresql://root:root@localhost:5431/orca_data')

df.to_sql(name='PPh3_test', con=engine, if_exists='replace')
