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

model_params = {
                'visibility': [True, False],
                "initial_explorers": range(1, 6, 2),
                "initial_competitors": [ 0, 3 , 5],
                "initial_predators": [ 0, 3, 5]
                # "initial_competitors": [ 0, 3, 5],
                # "initial_predators": [ 0, 3, 5]
                #
}

# var_model_params = {
#                 'visibility': [True, False],
#                 "initial_explorers": range(1, 5),
#                 "initial_competitors": range(0, 5),
#                 "initial_predators": range(0, 5)
#                 }

br = BatchRunner(PsyRTSGame,
                 model_params,
                 iterations= 50,
                 max_steps=150,
                 model_reporters={"Data Collector": lambda m: m.datacollector})


if __name__ == '__main__':
    br.run_all()
    br_df = br.get_model_vars_dataframe()
    #br_step_data =  br_df
    br_step_data = pd.DataFrame()

    for i in range(len(br_df["Data Collector"])):
        print("columna")
        print(br_df["Data Collector"][i].get_model_vars_dataframe().columns )
        if isinstance(br_df["Data Collector"][i], DataCollector):
            print (br_df["Data Collector"][i].get_model_vars_dataframe().describe())
            i_run_data = br_df["Data Collector"][i].get_model_vars_dataframe()
            br_step_data = br_step_data.append(i_run_data, ignore_index=True)
    br_step_data.to_csv("PsyRTSModelBorrar.csv")
