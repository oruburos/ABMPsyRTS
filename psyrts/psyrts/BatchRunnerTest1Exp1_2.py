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

model_paramsT = {
                'visibility': [True, False],
                "initial_explorers": range(1, 6, 2),
                "initial_competitors": [ 0 ],
                "initial_predators": [ 0]
}

model_paramsP = {
                'visibility': [ False],
                "initial_explorers": range(1, 6, 2),
                "initial_competitors": [ 0, 3 , 5],
                "initial_predators": [ 0, 3, 5]
                # "initial_competitors": [ 0, 3, 5],
                # "initial_predators": [ 0, 3, 5]
                #
}


br = BatchRunner(PsyRTSGame,
                 model_paramsT,
                 iterations= 1,
                 max_steps=150,
                 model_reporters={"Data Collector": lambda m: m.datacollector})

if __name__ == '__main__':
    br.run_all()
    br_df = br.get_model_vars_dataframe()
    #br_step_data =  br_df
    br_step_data = pd.DataFrame()

    for i in range(len(br_df["Data Collector"])):
        if isinstance(br_df["Data Collector"][i], DataCollector):
            i_run_data = br_df["Data Collector"][i].get_model_vars_dataframe()
            br_step_data = br_step_data.append(i_run_data, ignore_index=True)

    concat = br_step_data
    concat.to_csv("PsyRTSTest1-2021.csv")
