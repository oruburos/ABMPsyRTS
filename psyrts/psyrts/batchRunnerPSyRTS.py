from psyrts.agents import Predator, Competitor, Participant, Resources, CentralPlace
from psyrts.model import PsyRTSGame, resources_competitors, resources_participants
from mesa.batchrunner import BatchRunner

model_params = {
                'visibility':False,
                "initial_explorers":  5,
                "initial_competitors":  5
                }

var_model_params = {
                "initial_predators": range(1, 5)
                }


#parameters = {"n_agents": range(1, 20)}
batch_run = BatchRunner (PsyRTSGame, fixed_parameters=model_params, variable_parameters= var_model_params, iterations=2, max_steps=100 )
batch_run.run_all()