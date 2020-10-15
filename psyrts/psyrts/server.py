from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from psyrts.agents import Predator, Competitor, Participant, Resources
from psyrts.model import PsyRTSGame

def psyrtsPortrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Competitor:
        portrayal["Shape"] = "psyrts/resources/competitor.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 3

    elif type(agent) is Participant:
        portrayal["Shape"] = "psyrts/resources/explorer.png"

        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Predator:
        portrayal["Shape"] = "psyrts/resources/predator.png"

        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text_color"] = "White"

    elif type(agent) is Resources:
        if agent.fully_grown:
            portrayal["Color"] = ["#12af44", "#00CC00", "#009900"]
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = .8
        portrayal["h"] = .8

    return portrayal


canvas_element = CanvasGrid(psyrtsPortrayal, 20, 20, 500, 500)
chart_element = ChartModule([{"Label": "Predator", "Color": "#AA0000"},
                             {"Label": "Participant", "Color": "#00AA00"},
                             {"Label": "Explorer", "Color": "#061166"}])

model_params = {
                "visibility": UserSettableParameter('checkbox', 'Total Visibility', True),
                "initial_predators": UserSettableParameter('slider', 'Number Predators ', 1, 1, 5),
                "initial_explorers": UserSettableParameter('slider', 'Number Explorers ' , 1, 1, 5),
                "initial_competitors": UserSettableParameter('slider', 'Number Competitors ', 1, 1, 5),
                }

server = ModularServer(PsyRTSGame, [canvas_element, chart_element], "PsyRTS Module", model_params)
server.port = 8521
