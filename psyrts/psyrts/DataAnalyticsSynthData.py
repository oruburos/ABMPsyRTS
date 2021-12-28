import pandas as pd
from sqlalchemy import create_engine


df = pd.read_csv("PsyRTSTest1Limpio.csv")

df_minimo= df[['experiment', 'condition_exp', 'Conditions',
       'ResourcesRatio', 'Exploitation', 'Exploration', 'balance_ee', 'performance', 'ProportionEE',
       'MapExplored']]


print(df_minimo.columns)

# print(df_minimo)


groups = df_minimo.groupby(['experiment', 'condition_exp'], group_keys=True).mean()
print(groups)
mysqlServer = 'mysql+pymysql://root:@localhost:3308/'
bdFinalData = "FinalDataPhD"

engine = create_engine(mysqlServer+bdFinalData)

groups.to_sql("visibilitysynthtest", con=engine, if_exists='replace', index=True)
