import pandas as pd
from sqlalchemy import create_engine


inputfile = "e4bisCORTO.csv"
outputfile = "E4_v2.csv"
df = pd.read_csv(inputfile)

df_minimo= df[['experiment', 'condition_exp', 'Conditions',
       'ResourcesRatio', 'Exploitation', 'Exploration', 'balance_ee', 'performance']]

print(df_minimo.columns)

groups = df_minimo.groupby(['experiment', 'condition_exp'], group_keys=True).mean()
print(groups)

groups.to_csv(outputfile)