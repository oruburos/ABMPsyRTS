from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from mesa.visualization.modules import TextElement
from psyrts.agents import Predator, Competitor, Participant, Resources, CentralPlace
from psyrts.model import PsyRTSGame, resources_competitors, resources_participants


def psyrtsPortrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Competitor:
        portrayal["Shape"] = "psyrts/resources/competitor.png"
        portrayal["scale"] = 0.6
        portrayal["Layer"] = 3

    elif type(agent) is Participant:
        portrayal["Shape"] = "psyrts/resources/explorer.png"
        portrayal["scale"] = 0.6
        portrayal["Layer"] = 1

    elif type(agent) is Predator:
        portrayal["Shape"] = "psyrts/resources/predator.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text_color"] = "White"

    elif type(agent) is Resources:
        portrayal["Color"] = ["#12af44"]
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["r"] = .6

    elif type(agent) is CentralPlace:
        if agent.fromParticipant:
            portrayal["Color"] = ["#009922"]
        else:
            portrayal["Color"] = ["#FFAA23"]
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["r"] = 1.8

    else:
        portrayal["Color"] = ["#AAAADD"]

    return portrayal


canvas_element = CanvasGrid(psyrtsPortrayal, 20, 20, 500, 500)
chart_element = ChartModule([                           {"Label": "Resources Competitor", "Color": "#00AA00"}                ]         )




class MyTextElement(TextElement):
    def render(self, model):

        totalResources = str(model.resources)
        resourcesParticipant = str(resources_participants(model))
        resourcesCompetitor = str(resources_competitors(model))

        return "Total Resources: {}<br> Resources Participant:{} <br> Resources Competitor: {}".format( totalResources , resourcesParticipant , resourcesCompetitor)

model_params = {
                "visibility": UserSettableParameter('checkbox', 'Total Visibility', True),
                "initial_explorers": UserSettableParameter('slider', 'Number Explorers ' , 1, 1, 5),
                "initial_competitors": UserSettableParameter('slider', 'Number Competitors ', 0, 0, 5),
                "initial_predators": UserSettableParameter('slider', 'Number Predators ', 0, 0, 5),

                }

server = ModularServer(PsyRTSGame, [canvas_element, MyTextElement() , chart_element], "PsyRTS Module", model_params)
server.port = 8521
