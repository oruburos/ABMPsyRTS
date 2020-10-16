from mesa import Agent
from psyrts.random_walk import RandomWalker

class Participant(RandomWalker):
    '''
    A Participant that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    '''

    withResources = False

    def __init__(self, unique_id, pos, model, moore , cp):
        super().__init__(unique_id, pos, model, moore=moore)
        self.carrying = False
        self.cp = cp

    def step(self):
        '''
        A model step. Move, then eat grass and reproduce.
        '''
        self.random_move()
        living = True


        if self.model.visibility:
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            #resourcesPlace = [obj for obj in this_cell if isinstance(obj, Resources)][0]


            # Death
            # if self.energy < 0:
            #     self.model.grid._remove_agent(self.pos, self)
            #     self.model.schedule.remove(self)
            #     living = False
            #
            # lamb = Participant(self.model.next_id(), self.pos, self.model,
            #                   self.moore, self.energy)
            # self.model.grid.place_agent(lamb, self.pos)
            # self.model.schedule.add(lamb)



class Competitor(RandomWalker):
    '''
    A Competitor that walks around,
    The init is the same as the RandomWalker.
    '''

    def __init__(self, unique_id, pos, model, moore , cp):
        super().__init__(unique_id, pos, model, moore=moore )
        self.carrying = False
        self.cp = cp
    def step(self):
        '''
        A model step. Move, then eat grass and reproduce.
        '''

        if not self.carrying:
            self.random_move()

            # If there are resources, forage
            this_cell = self.model.grid.get_cell_list_contents([self.pos])



            for obj in this_cell:
                if isinstance(obj, Resources):
                    resourcesPellet = obj
                    resourcesP = resourcesPellet.resources
                    if resourcesP >3:
                        resourcesPellet.resources = resourcesPellet.resources- 3
                        self.resources = resourcesP
                    else:
                        self.resources = resourcesP
                        resourcesPellet.resources = 0
                    self.carrying = True
        else:
            print("go to central place")
            self.move_towards( self.cp)
            # If there are resources, forage
            this_cell = self.model.grid.get_cell_list_contents([self.pos])

            for obj in this_cell:
                if isinstance(obj, CentralPlace):
                    centralPlaceMine = obj
                    centralPlaceMine.resources = centralPlaceMine.resources + self.resources
                    self.resources= 0
                    self.carrying =False
                    self.model.resourcesCompetitor =centralPlaceMine.resources
                    print(" Actualizando resources competitor " + str(centralPlaceMine.resources))

class Predator(RandomWalker):
    '''
    A Predator that walks around
    '''

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)

    def step(self):
        self.random_move()



        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        sheep = [obj for obj in this_cell if isinstance(obj, Competitor) or isinstance(obj, Participant)]

        if len(sheep) > 0:
            sheep_to_eat = self.random.choice(sheep)
            self.model.grid._remove_agent(self.pos, sheep_to_eat)
            self.model.schedule.remove(sheep_to_eat)


class Resources(Agent):
    '''
    A patch of Resources that grows at a fixed rate and it is eaten by competitors and participants
    '''

    def __init__(self, unique_id, pos, model, fully_grown, current_resources):
        '''
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        '''
        super().__init__(unique_id, model)
        self.fully_grown = True
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

    #def step(self):


