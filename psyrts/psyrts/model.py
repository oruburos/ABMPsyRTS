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
    sheep_reproduce = 0.04
    wolf_reproduce = 0.05

    wolf_gain_from_food = 20

    grass = False
    grass_regrowth_time = 300
    sheep_gain_from_food = 4

    verbose = False  # Print-monitoring

    description = 'A model for simulating participants running the different experiments.'

    def __init__(self, height=20, width=20,initial_participants=1,
                 initial_sheep=1, initial_wolves=1,
                 sheep_reproduce=0.0, wolf_reproduce=0.0,
                 wolf_gain_from_food=20,
                 grass=False, grass_regrowth_time=300, sheep_gain_from_food=500):
        '''
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_participants: Number of units each participant knows
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        '''
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_participants = initial_participants
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.datacollector = DataCollector(
            {"Predators": lambda m: m.schedule.get_breed_count(Predator),
             "Competitors": lambda m: m.schedule.get_breed_count(Competitor)})

        # Create sheep:
        for i in range(self.initial_sheep):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.sheep_gain_from_food)
            sheep = Competitor(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(sheep, (x, y))
            self.schedule.add(sheep)

        # Create wolves
        for i in range(self.initial_wolves):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.wolf_gain_from_food)
            wolf = Predator(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(wolf, (x, y))
            self.schedule.add(wolf)

        # Create grass patches
        if self.grass:
            locations = [(4,3) , (16,3), (3,10) , (10,10),(17,10) , (16,17),(4,17) , ]
            #for agent, x, y in self.grid.coord_iter():
            for pa in locations:
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
            print('Final number wolves: ',
                  self.schedule.get_breed_count(Predator))
            print('Final number sheep: ',
                  self.schedule.get_breed_count(Competitor))
