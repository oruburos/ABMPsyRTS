from mesa import Agent
from psyrts.random_walk import RandomWalker
from random import randrange, uniform

class Participant(RandomWalker):
    '''
    A Participant that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    '''

    def __init__(self, unique_id, pos, model, moore , cp):
        super().__init__(unique_id, pos, model, moore=moore)
        self.carrying = False
        self.cp = cp
        self.futurepos = (0, 0)
        self.goal()

        self.predatorPerceived =False
        self.competitorPerceived = False

        self.threshold = 0.0



    def goal(self):

        x = randrange(3, 18)  # tecleo cerca, no lejos
        y = randrange(3, 18)
        # x = randrange(-6, 6) #tecleo cerca, no lejos
        # y = randrange(-6, 6)
        #
        # newpos = (self.pos[0] + x , self.pos[1] +y )
        #
        # if self.model.grid.out_of_bounds( newpos):
        #     x = randrange(3, 18)  # tecleo cerca, no lejos
        #     y = randrange(3, 18)
        #     self.futurepos = (x, y)
        # else:
        #     self.futurepos = (x, y)

        self.futurepos = (x, y)

    def seePredator(self):
        return self.vision(Predator)


    def vision(self, type):


        stop = randrange(1, 10)
        if stop > 2:

            next_moves=[]
            if self.model.visibility:
                next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True,2 )#2 ok

            else:
                next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True, 1) #1ok

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

    def updateModel(self):

        self.threshold = 0.0
        if self.predatorPerceived:
            self.threshold = self.threshold +.2
        if self.competitorPerceived:
            self.threshold =  self.threshold +.1
        self. threshold =  self.threshold +self.model.noise

    def step(self):
        '''
        A model step. Move, then forage.
        '''


        self.updateModel()


        enemy = self.seePredator()
        if enemy:
            #print("Move away from predator")
            self.move_away(enemy)

        else:
            if not self.carrying:

                seeResources = self.seeResources()
                if seeResources:
                    noise = self.random.random()
                    if noise < self.threshold:
                       # print("uncertain")
                        self.random_move()
                    else:
                        self.move_towards(seeResources)
                    # If there are resources, forage
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
                else:
                    noise = self.random.random()
                    if noise < self.threshold:
                        # print("uncertain")
                        self.random_move()
                    else:
                        self.move_towards(self.futurepos)

                    if self.pos == self.futurepos:
                        self.goal()
            else:

                #  print("go to central place")

                noise = self.random.random()
                if noise < self.threshold:
                   # print("uncertain")
                    self.random_move()
                else:
                    self.move_towards(self.cp.pos)

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
                               # print(" Actualizando resources participant " + str(self.model.resourcesParticipants))

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        for obj in this_cell:
            if isinstance(obj, BreadCrumb):
                if self.pos in self.model.locationsExploitation:

                    self.model.stepsExploiting = self.model.stepsExploiting + 1
                else:
                    #self.model.stepsExploring = self.model.stepsExploring + 1
                    if not obj.visited:
                        self.model.stepsExploring = self.model.stepsExploring + 1
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
        x = randrange(0 , 19)
        y = randrange(0 , 19)
        self.futurepos = ( x,y)


    def seePredator(self):
        return self.vision(Predator)


    def vision(self, type):
        next_moves = []
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True, 3)

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
                noise = randrange(1, 3)
                #print("Noise")
                if noise <3 :
                   # print("noise")
                    self.random_move()
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
                noise = randrange(1, 2)
                #print("Noise")
                if noise == 1 :
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


class Predator(RandomWalker):
    '''
    A Predator that walks around
    '''
    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)
        self.futurepos = (0, 0)


    def seePrey(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)

        for cells in next_moves:

            this_cell = self.model.grid.get_cell_list_contents(cells)
            for obj in this_cell:
                if isinstance(obj, Competitor) or isinstance(obj, Participant):
                    return obj.pos

        return None

    def step(self):

        posPrey = self.seePrey()

        if posPrey:

            #self.move_towards(posPrey)
            kind = randrange(1,3)

            if kind >1:
                self.move_towards(posPrey)
            else:
                self.random_move()
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        sheep = [obj for obj in this_cell if isinstance(obj, Competitor) or isinstance(obj, Participant)]

        if len(sheep) > 0:
            sheep_to_eat = self.random.choice(sheep)
            kill = randrange(1, 5)

            if kill == 1 :
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
