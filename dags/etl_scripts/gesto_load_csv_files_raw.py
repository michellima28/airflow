import glob
import pandas as pd
from sqlalchemy import create_engine

# copy csv files data to a pandas dataframe
files = glob.glob("/home/michel/airflow/dags/files/contas_*.csv")
#dfs = [pd.read_csv(f, header=None, sep=";") for f in files]
dfs = [pd.read_csv(f, sep=";") for f in files]

df_contas = pd.concat(dfs,ignore_index=True)
print(df_contas)

# load dataframe data to postgres table
engine = create_engine('postgresql://dbuser:12345@localhost:5432/localdb')
df_contas.to_sql('contas', engine, if_exists='replace', index=False)
