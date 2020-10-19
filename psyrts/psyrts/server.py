from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from mesa.visualization.modules import TextElement
from psyrts.agents import Predator, Competitor, Participant, Resources, CentralPlace, BreadCrumb
from psyrts.model import PsyRTSGame, resources_competitors, resources_participants , exploration, exploitation, resourcesRatio, proportionEE, mapExplored
from mesa.batchrunner import BatchRunner

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

    elif type(agent) is BreadCrumb:
        if agent.visited:
            portrayal["Color"] = ["#0cccc0"]
        else:
            portrayal["Color"] = ["#EEEEEE"]
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["r"] = .3

    else:
        portrayal["Color"] = ["#AAAADD"]

    return portrayal


canvas_element = CanvasGrid(psyrtsPortrayal, 20, 20, 500, 500)
chart_element = ChartModule([                           {"Label": "Exploration", "Color": "#00AA00"}    , {"Label": "Exploitation", "Color": "#0041FF"}       , {"Label": "ResourcesRatio", "Color": "#FFAA22"}     , {"Label": "MapExplored", "Color": "#00FFFF"}      ]         )



class MyTextElement(TextElement):
    def render(self, model):

        totalResources = str(model.resources)
        explorationS = exploration(model)
        exploitationS = exploitation(model)
        resourceRatio = resourcesRatio(model)
        if  explorationS+exploitationS == 0:
            balance = ( explorationS-exploitationS) /.2
        else:
            balance = (explorationS - exploitationS) / ((explorationS + exploitationS))
        resourcesParticipant = str(resources_participants(model))
        actividad = proportionEE(model)
        resourcesCompetitor = str(resources_competitors(model))
        performance = exploitationS +explorationS
        mapcoverage = mapExplored(model)

        #return "Total Resources: {} Resources Part:{}  Resources Co: {}  <br>  Ratio :{:2.3f}   Exploration :{:2.3f} Exploitation:{:2.3f}  Performance {:2.3f} <br>  Proportion :{:2.3f} Balance: {:2.3f}".format( totalResources , resourcesParticipant , resourcesCompetitor, resourceRatio, explorationS, exploitationS,performance, actividad, balance )
        return "<br>Total Resources: {} Resources Participant:{} Resources Competitor:{}" \
               "<br>   Ratio :{:2.3f} <br>  Exploration :{:2.3f} Exploitation:{:2.3f}  Performance {:2.3f} <br>  Proportion Map Explored :{:2.3f} <br> Balance: {:2.3f} ".format(
            totalResources, resourcesParticipant, resourcesCompetitor, resourceRatio, explorationS, exploitationS,
            performance, mapcoverage, balance)

model_params = {
                "visibility": UserSettableParameter('checkbox', 'Total Visibility', False),
                "initial_explorers": UserSettableParameter('slider', 'Number Explorers ' , 5, 1, 5),
                "initial_competitors": UserSettableParameter('slider', 'Number Competitors ', 5, 0, 5),
                "initial_predators": UserSettableParameter('slider', 'Number Predators ', 0 , 0, 5),

                "impactTotalVisibility": UserSettableParameter('slider', 'impactTotalVisibility ', 0.35, 0, 1, .05 ),
                "impactPartialVisibility": UserSettableParameter('slider', 'impactPartialVisibility ', 0.35, 0, 1, .05 ),
                "impactParticipants": UserSettableParameter('slider', 'impactParticipants ', 0.25, 0, .5, .01),
                "impactCompetitors": UserSettableParameter('slider', 'impactCompetitors ', 0.05, 0, .25, .01),
                "impactPredators": UserSettableParameter('slider', 'impactPredators ', 0.05, 0, .25, .01)
                }

server = ModularServer(PsyRTSGame, [canvas_element, MyTextElement() , chart_element ], "PsyRTS Module", model_params)
server.port = 8521
