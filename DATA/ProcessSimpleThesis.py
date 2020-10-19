import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import json


#
# experiment = 2
#
mysqlServer ='mysql+pymysql://root:@localhost:3308/'
bdFinalData = "FinalDataPhD"

engine = create_engine(mysqlServer+bdFinalData)
#df = pd.read_csv("PsyRTSModelBorrar.csv")
df = pd.read_csv("finaldataphd.csv",sep=';')

print (df.shape)

print (df.columns)
print( df.head(3))

df = df[['experiment', 'condition_exp', 'partialvisibility',
       'explorers', 'competitors', 'predators', 'resources_ratio',  'exploitation', 'exploration', 'balance_ee','performance']]

print (df.shape)
print (df.columns)
print( df.head(3))
df.to_csv("SimplestData.csv")

#
# pd.set_option("display.max_colwidth", None)
# #df.to_sql('prolificE{}'.format(experiment),con= engine ,if_exists ='append' , index= False)
#
# print(df.shape)
# df2 = df.groupby(['Experiment_Synth'])['Step'].max().reset_index()
#
# for row in df2.itertuples():
#     #print(row.Experiment_Synth)
#     #print(row.Step)
#     indexNames = df[ (df['Step'] < row.Step) & (df['Experiment_Synth'] == row.Experiment_Synth) ].index
#     df.drop(indexNames , inplace=True)
#
# print(df.shape)
#
# def checkcondition( row ):
#
#     condici = row['Conditions']
#     condiciones = eval(condici)
#
#     experiment = -1
#     condition = -1
#     competitors = int(condiciones[0])
#     explorers = int(condiciones[1])
#     predators  = int(condiciones[2])
#     visibilidad = bool(condiciones[3])
#
#
#     if visibilidad:
#         if predators>0 or competitors > 0 :
#             experiment = -1
#             condition = -1
#         else:
#             if explorers == 1:
#                 experiment = 3
#                 condition = 1
#             if explorers == 3:
#                 experiment = 3
#                 condition = 3
#             if explorers == 5:
#                 experiment = 1
#                 condition = 1
#     else:
#         if predators == 0 and competitors == 0:
#             if explorers == 1:
#                 experiment = 3
#                 condition = 2
#             if explorers == 3:
#                 experiment = 3
#                 condition = 4
#             if explorers == 5:
#                 experiment = 1
#                 condition = 2
#
#         elif   predators == 0 and competitors == 5:
#
#               if explorers == 5:
#                 experiment = 1
#                 condition = 4
#         elif predators == 3 and competitors == 0:
#
#             if explorers == 5:
#                 experiment = 1
#                 condition = 3
#
#         elif   predators == 5 and competitors == 3:
#
#             if explorers == 5:
#                 experiment = 4
#                 condition = 3
#             if explorers == 3:
#                     experiment = 4
#                     condition = 1
#
#         elif predators == 3 and competitors == 5:
#             if explorers == 5:
#                 experiment = 1
#                 condition = 5
#             if explorers == 3:
#                 experiment = 4
#                 condition = 2
#
#
#     return    pd.Series( [experiment , condition])
#
#
# def balanceperformance(row):
#     exploration = float (row['Exploration'])
#     exploitation = float (row['Exploitation'])
#     balance =  (exploration- exploitation)/(exploration + exploitation)
#     performance = exploration+ exploitation
#
#     return pd.Series([balance, performance])
#
#
#
#
#
# df[['experiment','condition_exp'] ] = df.apply(checkcondition, axis=1)
#
#
# print(df.shape)
# indexNames = df[(df['condition_exp'] == -1 )].index
# df.drop(indexNames, inplace=True)
#
# df[['balance_ee','performance'] ] = df.apply(balanceperformance, axis=1)
#
# print(df.shape)
# df.to_csv("PsyRTSTest1Limpio.csv")
#
#
#
#
# #df.to_sql("experiments_generative_model",con= engine ,if_exists ='replace' , index= False)
# #df.to_sql("experiments_generative_model",conn)
#
