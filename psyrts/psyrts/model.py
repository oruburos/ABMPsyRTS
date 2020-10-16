
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from random import randrange, uniform

from psyrts.agents import Competitor, Predator, Participant, Resources, CentralPlace, BreadCrumb
from psyrts.schedule import RandomActivationByBreed


def exploration(model):
    return   (number_visited( model, True) )/328

def exploitation(model):
    return   (number_visited( model, False) )/72


def get_all_cell_contents(grid):
    return list(grid.iter_cell_list_contents(grid.G))


def iter_cell_list_contents( grid, cell_list):
        list_of_lists = [grid.G.node[node_id]['agent'] for node_id in cell_list if not grid.is_cell_empty(node_id)]
        return [item for sublist in list_of_lists for item in sublist]

def number_visited(model ,mode_exploration=True):
    #return sum([1 for a in get_all_cell_contents(model.grid) if a.visited is True])


    next_moves = []
    if mode_exploration:
        next_moves = model.locationsExploration
    else:
        next_moves = model.locationsExploitation
    print( "size grid " + str(len(next_moves)))
    visitadas = 0
    for cells in next_moves:
        this_cell = model.grid.get_cell_list_contents(cells)
        for obj in this_cell:
            if isinstance(obj, BreadCrumb):
                if obj.visited:
                    visitadas = visitadas + 1

    return visitadas


def resources_competitors(model):
    return model.resourcesCompetitors

def resources_participants(model):
    return model.resourcesParticipants

class PsyRTSGame(Model):


    height = 20
    width = 20

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

        self.fps = 0
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


        self.TotalCells = next_moves = self.grid.get_neighborhood( (10,10), True, True, 11)
        locationsResources = [(4,3) , (16,3), (3,10) , (10,10),(17,10) , (16,17),(4,17)  ]

        locationCPCompetitor = (10, 3)
        locationCPParticipant = (10, 17)

        self.locationsExploitation =[]

        for loc in locationsResources:#resources
            self.locationsExploitation = self.locationsExploitation + self.grid.get_neighborhood(loc, True, True,1)

        #cfp
        self.locationsExploitation = self.locationsExploitation + self.grid.get_neighborhood(locationCPParticipant, True, True, 1)
        #print( "size grid exploiit " + str(len(self.locationsExploitation)))

        self.locationsExploration =  list(set(self.TotalCells) - set(self.locationsExploitation))
        #print("size grid explore " + str(len(self.locationsExploration)))
        locationsParticipants = [(10, 15), (13, 15), (7, 15), ( 8, 15), (12, 15)  ]
        locationsCompetitors = [(10, 5), (13, 5), (7, 5), ( 8, 5), (12, 5) ]
        locationsPredators = [(10, 10), (13, 10), (7, 10), ( 8, 10), (12, 10) ]

        self.datacollector = DataCollector(
            model_reporters={"Exploration": exploration , "Exploitation": exploitation})   #reporto a datos

        centralplaceparticipant = CentralPlace(self.next_id(), locationCPParticipant, self, True)
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
             irand = randrange(1, 10)
             #irand = 4
           #  print("resource con valores {} ". format(  irand)  )
             self.resources = self.resources + irand
             patch = Resources(self.next_id(), pa, self, irand)
             self.grid.place_agent(patch, pa)
             self.schedule.add(patch)

        for x in range(0,20):
            for y in range(0, 20):
                breadcrumb = BreadCrumb(self.next_id(), (x,y), self)
                self.grid.place_agent(breadcrumb, (x,y))
                self.schedule.add(breadcrumb)

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

        # pellets = self.schedule.get_breed_count(Resources)
        # if pellets <=0:
        #     print("No more resources")
        #     self.running = False



        if self.resourcesCompetitors +self.resourcesParticipants == self.resources:
            print("Stop No More Resources")
            self.running = False

        if self.schedule.steps>150:
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
