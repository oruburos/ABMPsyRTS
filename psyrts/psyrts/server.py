from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from psyrts.agents import Predator, Competitor, Participant, Resources
from psyrts.model import PsyRTSGame


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Competitor:
        portrayal["Shape"] = "psyrts/resources/competitor.png"
        # https://icons8.com/web-app/433/sheep
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Participant:
        portrayal["Shape"] = "psyrts/resources/explorer.png"
        # https://icons8.com/web-app/433/sheep
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Predator:
        portrayal["Shape"] = "psyrts/resources/predator.png"
        # https://icons8.com/web-app/36821/German-Shepherd
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "White"

    elif type(agent) is Resources:
        if agent.fully_grown:
            portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule([{"Label": "Predator", "Color": "#AA0000"},
                             {"Label": "Participant", "Color": "#00AA00"},
                             {"Label": "Participant", "Color": "#061166"}])

model_params = {"grass": UserSettableParameter('checkbox', 'Grass Enabled', True),
                "grass_regrowth_time": UserSettableParameter('slider', 'Grass Regrowth Time', 20, 20, 50),
                "initial_sheep": UserSettableParameter('slider', 'Initial Sheep Population', 1, 1, 5),
                "sheep_reproduce": UserSettableParameter('slider', 'Sheep Reproduction Rate', 0.00, 0.01, 1.0,
                                                         0.01),
                "initial_wolves": UserSettableParameter('slider', 'Initial Wolf Population', 1, 1, 5),
                "initial_participants": UserSettableParameter('slider', 'Initial Wolf Population', 1, 1, 5),
                "wolf_reproduce": UserSettableParameter('slider', 'Wolf Reproduction Rate', 0.00, 0.01, 1.0,
                                                        0.01,
                                                        description="The rate at which wolf agents reproduce."),
                "wolf_gain_from_food": UserSettableParameter('slider', 'Wolf Gain From Food Rate', 20, 1, 50),
                "sheep_gain_from_food": UserSettableParameter('slider', 'Sheep Gain From Food', 4, 1, 10)}

server = ModularServer(PsyRTSGame, [canvas_element, chart_element], "PsyRTS Module", model_params)
server.port = 8521
