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
from random import randrange, uniform


from psyrts.agents import Competitor, Predator, Participant, Resources, CentralPlace
from psyrts.schedule import RandomActivationByBreed


def resources_competitors(model):
    return model.resourcesCompetitors

def resources_participants(model):
    return model.resourcesParticipants

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

        Args
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

        self.resources= 0
        self.resourcesParticipants =0
        self.resourcesCompetitors = 0

        locationsResources = [(4,3) , (16,3), (3,10) , (10,10),(17,10) , (16,17),(4,17)  ]
        locationsParticipants = [(10, 15), (13, 15), (7, 15), ( 8, 15), (12, 15)  ]
        locationsCompetitors = [(10, 5), (13, 5), (7, 5), ( 8, 5), (12, 5) ]
        locationsPredators = [(10, 10), (13, 10), (7, 10), ( 8, 10), (12, 10) ]

        locationCPCompetitor = (10, 3)
        locationCPParticipant= (10, 17)

        # self.datacollector = DataCollector(
        #     {"Predators": lambda m: m.schedule.get_breed_count(Predator),
        #      "Competitors": lambda m: m.resourcesCompetitors,
        #      "Explorers": lambda m: m.resourcesParticipant,
        #      "Resources": lambda m: m.schedule.get_breed_count(Competitor)})

        self.datacollector = DataCollector(
            {
             # "Res Competitor": resources_competitors,
             #  "Res Participant":   resources_participants
            })

        centralplaceparticipant = CentralPlace(self.next_id(), locationCPParticipant, self)
        self.grid.place_agent(centralplaceparticipant, locationCPParticipant)
        self.schedule.add(centralplaceparticipant)

        centralplacecompetitor = CentralPlace(self.next_id(), locationCPCompetitor, self, False)
        self.grid.place_agent(centralplacecompetitor, locationCPCompetitor)
        self.schedule.add(centralplacecompetitor)

        # Create competitor:
        for i in range(self.initial_competitors):
            sheep = Competitor(self.next_id(), locationsCompetitors[i], self, True, centralplacecompetitor)
            self.grid.place_agent(sheep, locationsCompetitors[i])
            self.schedule.add(sheep)

        # Create explorers:
        for i in range(self.initial_explorers):
            sheep = Participant(self.next_id(), locationsParticipants[i], self, True, centralplaceparticipant)
            self.grid.place_agent(sheep, locationsParticipants[i])
            self.schedule.add(sheep)

        # Create predators
        for i in range(self.initial_predators):
            wolf = Predator(self.next_id(), locationsPredators[i], self, True)
            self.grid.place_agent(wolf, locationsPredators[i])
            self.schedule.add(wolf)

        for pa in locationsResources:
             # randrange gives you an integral value
            # irand = randrange(1, 10)
             irand = 4
           #  print("resource con valores {} ". format(  irand)  )
             self.resources = self.resources + irand
             patch = Resources(self.next_id(), pa, self, irand)
             self.grid.place_agent(patch, pa)
             self.schedule.add(patch)


        self.running = True
        self.datacollector.collect(self)


    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        participantsAlive = self.schedule.get_breed_count(Participant)
        if participantsAlive <=0:
            print("Stop Participants dead")
            self.running = False

        if self.resourcesCompetitors +self.resourcesParticipants == self.resources:
            print("Stop No More Resources")
            self.running = False

        # if self.verbose:
        #     print([self.schedule.time,
        #            self.schedule.get_breed_count(Predator),
        #            self.schedule.get_breed_count(Competitor)])

    def run_model(self, step_count=300):
        for i in range(step_count):
            self.step()

        # if self.verbose:
        #     print('')
        #     print('Resources by Participant: ',   self.schedule.get_breed_count(Participant))
        #     print('Resources by Competitors: ',   self.schedule.get_breed_count(Competitor))
        #     print('Explorers Alive: ', self.schedule.get_breed_count(Participant))
        #     print('Competitors Alive: ', self.schedule.get_breed_count(Competitor))
