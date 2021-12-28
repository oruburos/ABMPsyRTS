from mesa import Agent
from psyrts.random_walk import RandomWalker
from random import randrange, uniform
import scipy.stats as ss
import numpy as np


class Participant(RandomWalker):
    '''
    A Participant that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    '''

    def __init__(self, unique_id, pos, model, moore , cp):
        super().__init__(unique_id, pos, model, moore=moore)
        self.id = unique_id
        self.carrying = False
        self.cp = cp
        self.futurepos = (0, 0)
        self.memory = []
        self.predatorPerceived = False
        self.competitorPerceived = False
        self.certainty = 0.0
        self.goal()

    def goal(self):
        proposedPos = self.randomPosScreen()
        if not self.model.visibility:
            while proposedPos in self.memory:
                proposedPos = self.randomPosScreen()

        self.futurepos = proposedPos


    def influencePredator(self):

        mu, sigma = self.model.impactPredators, 0.001  # mean and standard deviation
        s = np.random.normal(mu, sigma)

        return s


    def uncertaintyInAgent(self):

        mu, sigma = 0.1, 0.02  # mean and standard deviation
        noise = np.random.normal(mu, sigma)
        s = noise
        if self.predatorPerceived:
            s = s +self.influencePredator()
        if self.competitorPerceived:
            s = s + self.influenceCompetitor()

        return s

    def influenceCompetitor(self):

        mu, sigma = self.model.impactPredators, 0.001  # mean and standard deviation
        s = np.random.normal(mu, sigma)
        return s

    def updateModel(self):

        self.certainty = 1.0-self.uncertaintyInAgent() - self.model.uncertainty


      #  print(" Certainty Control Agent" + str(self.certainty))

    def seePredator(self):

                next_moves  = self.model.grid.get_neighborhood(self.pos, self.moore, True, 1)  # 1ok

                for cells in next_moves:

                    this_cell = self.model.grid.get_cell_list_contents(cells)
                    for obj in this_cell:
                        if isinstance(obj, Predator):
                            return obj.pos
                return None




    def vision(self, type):

        stop = randrange(1, 8)
        if stop > -1:  #not always participants are doing something

            next_moves=[]
            if self.model.visibility:
                next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True, 3 )#2 ok

            else:
                next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True, 2) #1ok

            for cells in next_moves:

                this_cell = self.model.grid.get_cell_list_contents(cells)
                for obj in this_cell:
                    if isinstance(obj, type):
                        return obj.pos
            return None
        else:
            return None



    def seeResources(self):
       return self.vision(Resources)

    def seeCompetitor(self):
        return self.vision(Competitor)


    def step(self):
        '''
        A model step. Move, then forage.
        '''

        #participants not always select an unit, and the more units, the more chances to not play it


        multitaskingFriction = (1 - self.model.impactParticipants ) ** self.model.initial_explorers

        useUnit = self.random.random()

        if useUnit < multitaskingFriction:

            self.updateModel()
            enemy = self.seePredator()
            if enemy:
                noise = self.random.random()
                if noise > self.certainty:
                    self.move_towards(self.futurepos)
                else:
                    self.move_away(enemy)
            else:
                if not self.carrying:
                    seeResources = self.seeResources()
                    if seeResources:

                        self.move_towards(seeResources)
                        # # If there are resources, forage
                        this_cell = self.model.grid.get_cell_list_contents([self.pos])

                        for obj in this_cell:

                            if isinstance(obj, Resources):
                                resourcesPellet = obj
                                resourcesP = resourcesPellet.resources
                                if resourcesP > 3:
                                    resourcesPellet.resources = resourcesPellet.resources - 3
                                    self.resources = 3
                                else:
                                    self.resources = resourcesP
                                    resourcesPellet.resources = 0
                                self.carrying = True
                    else:# no resources on sight
                            noise = self.random.random()
                            if noise > self.certainty:
                                self.goal()

                            self.move_towards(self.futurepos)

                else:
                    noise = self.random.random()
                    if noise < self.certainty:
                        self.move_towards(self.cp.pos)
                    else:
                        self.move_towards(self.futurepos)

                   # print("Participant move to central place " + str(self.cp.pos))
                    this_cell = self.model.grid.get_cell_list_contents([self.pos])
                    for obj in this_cell:
                        if isinstance(obj, CentralPlace):
                            centralPlaceMine = obj
                            if centralPlaceMine.fromParticipant:
                                if centralPlaceMine == self.cp:
                                    centralPlaceMine.resources = centralPlaceMine.resources + self.resources
                                    self.resources = 0
                                    self.carrying = False
                                    self.model.resourcesParticipants = centralPlaceMine.resources
                                    self.goal()

            this_cell = self.model.grid.get_cell_list_contents([self.pos])

            self.memory.append(self.pos)
            if self.pos == self.futurepos:
                self.goal()

            for obj in this_cell:
                if isinstance(obj, BreadCrumb):
                    if self.pos in self.model.locationsExploitation:
                        self.model.stepsExploiting = self.model.stepsExploiting + 1
                    else:
                        # if self.carrying:
                        #     self.model.stepsExploiting = self.model.stepsExploiting + 1
                        # else:
                        #     self.model.stepsExploring = self.model.stepsExploring + 1
                        self.model.stepsExploring = self.model.stepsExploring + 1

                    if not obj.visited:
                        obj.visited = True
                    return



class Competitor(RandomWalker):
    '''
    A Competitor that walks around,
    The init is the same as the RandomWalker.
    '''

    def __init__(self, unique_id, pos, model, moore , cp):
        super().__init__(unique_id, pos, model, moore=moore )
        self.carrying = False
        self.cp = cp
        self.futurepos = (0,0)
        self.goal()

    def goal(self):
        # x = randrange(0 , 19)
        # y = randrange(0 , 19)
        self.futurepos = self.randomPos()


    def seePredator(self):
        return self.vision(Predator)


    def vision(self, type):
        next_moves = []
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True, 1)

        for cells in next_moves:

            this_cell = self.model.grid.get_cell_list_contents(cells)
            for obj in this_cell:
                if isinstance(obj, type):
                    return obj.pos
        return None

    def seeResources(self):
       return self.vision(Resources)

    def step(self):
        '''
        A model step. Move, then forage.
        '''

        enemy = self.seePredator()
        if enemy:
            self.move_away(enemy)

        if not self.carrying:
            seeResources = self.seeResources()
            if seeResources:
                noise = randrange(1, 5)

                if noise <3 :
                   # print("noise")
                    self.random_move()
                else:
                    self.move_towards(seeResources)
                # If there are resources, forage
                this_cell = self.model.grid.get_cell_list_contents([self.pos])

                for obj in this_cell:
                    if isinstance(obj, Resources):
                        resourcesPellet = obj
                        resourcesP = resourcesPellet.resources
                        if resourcesP >3:
                            resourcesPellet.resources = resourcesPellet.resources- 3
                            self.resources = 3
                        else:
                            self.resources = resourcesP
                            resourcesPellet.resources = 0
                        self.carrying = True
            else:
                noise = randrange(1, 4)
                #print("Noise")
                if noise < 2 :
                   # print("noise")
                    self.random_move()
                else:
                    self.move_towards(self.futurepos)
                if self.pos == self.futurepos:
                    self.goal()
        else:

          #  print("go to central place")
            self.move_towards( self.cp.pos)

            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            for obj in this_cell:
                if isinstance(obj, CentralPlace):
                    centralPlaceMine = obj
                    if not centralPlaceMine.fromParticipant:
                        if centralPlaceMine == self.cp:
                            centralPlaceMine.resources = centralPlaceMine.resources + self.resources
                            self.resources= 0
                            self.carrying =False
                            self.model.resourcesCompetitors = centralPlaceMine.resources
                           # print(" Actualizando resources competitor " + str(self.model.resourcesCompetitors))
                            self.goal()

class Predator(RandomWalker):
    '''
    A Predator that walks around
    '''
    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)
        self.futurepos = (0, 0)


    def seePrey(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)

        preys = []
        for cells in next_moves:

            this_cell = self.model.grid.get_cell_list_contents(cells)
            for obj in this_cell:
                if isinstance(obj, Competitor) or isinstance(obj, Participant):
                    preys.append(obj.pos)

        if len(preys) > 0:
            return self.random.choice(preys)
        else:
            return None

    def step(self):

        posPrey = self.seePrey()

        if posPrey:

            #self.move_towards(posPrey)
            kind = randrange(0,10)

            if kind <2:
                self.move_towards(posPrey)
            else:
                self.random_move()
        #x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        sheep = [obj for obj in this_cell if isinstance(obj, Competitor) or isinstance(obj, Participant)]

        if len(sheep) > 0:
            sheep_to_eat = self.random.choice(sheep)
            kill = randrange(0, 20)

            if kill < 2 :
                self.model.grid._remove_agent(self.pos, sheep_to_eat)
                self.model.schedule.remove(sheep_to_eat)


class Resources(Agent):
    '''
    A patch of Resources that is foraged by competitors and participants
    '''

    def __init__(self, unique_id, pos, model,  current_resources):
        '''
        '''
        super().__init__(unique_id, model)
        self.resources = current_resources
        self.pos = pos
    def step(self):
        if self.resources <= 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)

class CentralPlace(Agent):
    '''
    A patch of Resources that grows at a fixed rate and it is eaten by competitors and participants
    '''

    def __init__(self, unique_id, pos, model, fromParticipant=True):
        '''
        Creates a new patch of grass
        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        '''
        self.resources = 0
        super().__init__(unique_id, model)
        self.fromParticipant = fromParticipant
        self.pos = pos



class BreadCrumb(Agent):

    def __init__(self, unique_id, pos, model, fromParticipant=True):
        '''
        Creates a new patch of grass
        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        '''
        self.visited = False
        super().__init__(unique_id, model)
