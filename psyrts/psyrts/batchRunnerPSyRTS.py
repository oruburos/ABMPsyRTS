from psyrts.agents import Predator, Competitor, Participant, Resources, CentralPlace
from psyrts.model import PsyRTSGame, resources_competitors, resources_participants

import itertools
from mesa import Model
from mesa.batchrunner import BatchRunner
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
import numpy as np
import pandas as pd

model_params = {
                'visibility': [True, False],
                "initial_explorers": range(1, 5),
                "initial_competitors": range(0, 5),
                "initial_predators": range(0, 5)
                }

var_model_params = {
                "initial_predators": range(1, 5)
                }


#
#
# # Start of datacollector functions
#
# def track_params(model):
#     return (model.init_people,
#             model.rich_threshold,
#             model.reserve_percent)
#
# def track_run(model):
#     return model.uid
#
#
# class BankReservesModel(Model):
#     # id generator to track run number in batch run data
#     id_gen = itertools.count(1)
#
#     # grid height
#     grid_h = 20
#     # grid width
#     grid_w = 20
#
#     """init parameters "init_people", "rich_threshold", and "reserve_percent"
#        are all UserSettableParameters"""
#     def __init__(self, height=grid_h, width=grid_w, init_people=2, rich_threshold=10,
#                  reserve_percent=50,):
#         self.uid = next(self.id_gen)
#         self.height = height
#         self.width = width
#         self.init_people = init_people
#         self.schedule = RandomActivation(self)
#         self.grid = MultiGrid(self.width, self.height, torus=True)
#         # rich_threshold is the amount of savings a person needs to be considered "rich"
#         self.rich_threshold = rich_threshold
#         self.reserve_percent = reserve_percent
#         # see datacollector functions above
#         self.datacollector = DataCollector(model_reporters={
#                                            "Rich": get_num_rich_agents,
#                                            "Poor": get_num_poor_agents,
#                                            "Middle Class": get_num_mid_agents,
#                                            "Savings": get_total_savings,
#                                            "Wallets": get_total_wallets,
#                                            "Money": get_total_money,
#                                            "Loans": get_total_loans,
#                                            "Model Params": track_params,
#                                            "Run": track_run},
#                                            agent_reporters={
#                                            "Wealth": lambda x: x.wealth})
#
#     def step(self):
#         # collect data
#         self.datacollector.collect(self)
#         # tell all the agents in the model to run their step function
#         self.schedule.step()
#
#     def run_model(self):
#         for i in range(self.run_time):
#             self.step()
#
#

br = BatchRunner(PsyRTSGame,
                 model_params,
                 iterations=2,
                 max_steps=150,
                 model_reporters={"Data Collector": lambda m: m.datacollector})

if __name__ == '__main__':
    br.run_all()
    br_df = br.get_model_vars_dataframe()
    #br_step_data =  br_df
    br_step_data = pd.DataFrame()
    for i in range(len(br_df["Data Collector"])):
        if isinstance(br_df["Data Collector"][i], DataCollector):
            print (br_df["Data Collector"][i].get_model_vars_dataframe().describe())
            i_run_data = br_df["Data Collector"][i].get_model_vars_dataframe()
            br_step_data = br_step_data.append(i_run_data, ignore_index=True)
    br_step_data.to_csv("PsyRTSModel.csv")
