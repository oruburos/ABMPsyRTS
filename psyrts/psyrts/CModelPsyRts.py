from psyrts.agents import Predator, Competitor, Participant, Resources, CentralPlace
from psyrts.model import PsyRTSGame, resources_competitors, resources_participants

import itertools
from mesa import Model
from mesa.batchrunner import BatchRunner, BatchRunnerMP
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
import numpy as np
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import json

def balanceperformance(row):
    exploration = float (row['Exploration'])
    exploitation = float (row['Exploitation'])
    balance =  (exploration- exploitation)/(exploration + exploitation)
    performance = exploration+ exploitation

    return pd.Series([balance, performance])

def checkcondition( row ):

    condici = str(row['Conditions'])
#    print(condici)
    condiciones = eval(condici)

    experiment = -1
    condition = -1
    competitors = int(condiciones[0])
    explorers = int(condiciones[1])
    predators  = int(condiciones[2])
    visibilidad = bool(condiciones[3])


    if visibilidad:
        if predators>0 or competitors > 0 :
            experiment = -1
            condition = -1
        else:
            if explorers == 1:
                experiment = 3
                condition = 1
            if explorers == 3:
                experiment = 3
                condition = 3
            if explorers == 5:
                experiment = 1
                condition = 1
    else:
        if predators == 0 and competitors == 0:
            if explorers == 1:
                experiment = 3
                condition = 2
            if explorers == 3:
                experiment = 3
                condition = 4
            if explorers == 5:
                experiment = 1
                condition = 2

        elif   predators == 0 and competitors == 5:

              if explorers == 5:
                experiment = 1
                condition = 4
        elif predators == 3 and competitors == 0:

            if explorers == 5:
                experiment = 1
                condition = 3

        elif   predators == 5 and competitors == 3:

            if explorers == 5:
                experiment = 4
                condition = 3
            if explorers == 3:
                    experiment = 4
                    condition = 1

        elif predators == 3 and competitors == 5:
            if explorers == 5:
                experiment = 1
                condition = 5
            if explorers == 3:
                experiment = 4
                condition = 2


    return    pd.Series( [experiment , condition])







#
#
# model_paramsT = {
#                 'visibility': [True, False],
#                 "initial_explorers": [1],
#                 "initial_competitors": [ 0 ],
#                 "initial_predators": [ 0]
# }


#
# model_paramsT = {
#                 'visibility': [True, False],
#                 "initial_explorers": [1 ,3 , 5],
#                # "initial_competitors": [ 0 ],
#                 #"initial_predators": [ 0],
#
#                 # "impactPartialVisibility": [.25],
#                  #"impactTotalVisibility": [.1],
#                 "impactParticipants": [.1 , .03 , .05 , .16 , .20, .23, .28]
#  }
#


model_paramsTEx3cond1 = {
                 'visibility': [True],
                "initial_explorers": [1],
                "impactParticipants": [.20],

}


model_paramsTEx3cond2 = {
                 'visibility': [False],
                "initial_explorers": [1],
                "impactParticipants": [.03],
}



model_paramsTEx3cond3 = {
                 'visibility': [True],
                "initial_explorers": [3],
                "impactParticipants": [.27],

}


model_paramsTEx3cond4 = {
                 'visibility': [False],
                "initial_explorers": [3],
                "impactParticipants": [.05],
}




model_paramsTEx3cond5 = {
                 'visibility': [True],
                "initial_explorers": [5],
                "impactParticipants": [.17],

}


model_paramsTEx3cond6 = {
                 'visibility': [False],
                "initial_explorers": [5],
                "impactParticipants": [.05],
}




model_paramsFixed = {

        "impactPartialVisibility": .25,
        "impactTotalVisibility": .1,

 }

nombreCSV = "model_paramsTEx3cond6"+".csv"
br = BatchRunner(PsyRTSGame,
                 variable_parameters=model_paramsTEx3cond6,
                 fixed_parameters= model_paramsFixed,
                 iterations= 50,
                 max_steps=150,
                 model_reporters={"Data Collector": lambda m: m.datacollector})

if __name__ == '__main__':
    br.run_all()
    br_df = br.get_model_vars_dataframe()
    br_step_data = pd.DataFrame()

    for i in range(len(br_df["Data Collector"])):
        if isinstance(br_df["Data Collector"][i], DataCollector):
            i_run_data = br_df["Data Collector"][i].get_model_vars_dataframe()
            br_step_data = br_step_data.append(i_run_data, ignore_index=True)

    concat = br_step_data
    df = concat
    df2 = df.groupby(['Experiment_Synth'])['Step'].max().reset_index()

    for row in df2.itertuples():
        indexNames = df[ (df['Step'] < row.Step) & (df['Experiment_Synth'] == row.Experiment_Synth) ].index
        df.drop(indexNames , inplace=True)


    df[['experiment','condition_exp'] ] = df.apply(checkcondition, axis=1)

    indexNames = df[(df['condition_exp'] == -1 )].index
    df.drop(indexNames, inplace=True)

    df[['balance_ee','performance'] ] = df.apply(balanceperformance, axis=1)

    df = df[['Experiment_Synth', 'experiment', 'condition_exp',  'Conditions',  'ResourcesRatio',  'Exploitation'  ,'Exploration',  'balance_ee', 'performance' ] ]
    df.to_csv(nombreCSV)


