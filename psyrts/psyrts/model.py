'''
Wolf-Sheep Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
'''

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from psyrts.agents import Competitor, Predator, Participant, Resources
from psyrts.schedule import RandomActivationByBreed


class PsyRTSGame(Model):


    height = 20
    width = 20
    initial_sheep = 3
    initial_wolves = 1
    initial_participants = 1
    visibility = False

    verbose = False  # Print-monitoring

    description = 'A model for simulating participants running the different experiments.'

    def __init__(self, height=20, width=20, visibility = False ,initial_competitors=1,
                 initial_explorers=1, initial_predators=1,):
        '''
        Create a new PsyRTS  model with the given parameters.

        Args:
            initial_competitors: Number of units each participant knows
            initial_explorers: Number of sheep to start with
            initial_predators: Number of wolves to start with
            visibility : total or partial visibility
        '''
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.visibility = visibility
        self.initial_competitors = initial_competitors
        self.initial_explorers = initial_explorers
        self.initial_predators = initial_predators

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=False)



        locationsResources = [(4,3) , (16,3), (3,10) , (10,10),(17,10) , (16,17),(4,17) , ]
        locationsParticipants = [(4, 3), (16, 3), (3, 10), (10, 10), (17, 10), (16, 17), (4, 17), ]
        locationsCompetitors = [(4, 3), (16, 3), (3, 10), (10, 10), (17, 10), (16, 17), (4, 17), ]
        locationsPredators = [(4, 3), (16, 3), (3, 10), (10, 10), (17, 10), (16, 17), (4, 17), ]

        self.datacollector = DataCollector(
            {"Predators": lambda m: m.schedule.get_breed_count(Predator),
             "Competitors": lambda m: m.schedule.get_breed_count(Competitor),
             "Explorers": lambda m: m.schedule.get_breed_count(Participant),
             "Resources": lambda m: m.schedule.get_breed_count(Competitor)})




        # Create competitor:
        for i in range(self.initial_competitors):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            sheep = Competitor(self.next_id(), (x, y), self, True)
            self.grid.place_agent(sheep, (x, y))
            self.schedule.add(sheep)

            # Create explorers:
            for i in range(self.initial_explorers):
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
                sheep = Participant(self.next_id(), (x, y), self, True)
                self.grid.place_agent(sheep, (x, y))
                self.schedule.add(sheep)

        # Create predators
        for i in range(self.initial_predators):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)

            wolf = Predator(self.next_id(), (x, y), self, True, 222)
            self.grid.place_agent(wolf, (x, y))
            self.schedule.add(wolf)



        for pa in locationsResources:
             fully_grown = True
             patch = Resources(self.next_id(), pa, self,fully_grown, 0)
             self.grid.place_agent(patch, pa)
             self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_breed_count(Predator),
                   self.schedule.get_breed_count(Competitor)])

    def run_model(self, step_count=300):

        if self.verbose:
            print('Initial number predators: ',
                  self.schedule.get_breed_count(Predator))
            print('Initial number competitors: ',
                  self.schedule.get_breed_count(Competitor))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Resources by Participant: ',   self.schedule.get_breed_count(Predator))
            print('Resources by Competitors: ',   self.schedule.get_breed_count(Competitor))
            print('Explorers Alive: ', self.schedule.get_breed_count(Competitor))
            print('Competitors Alive: ', self.schedule.get_breed_count(Competitor))
