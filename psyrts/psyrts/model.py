
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from random import randrange, uniform
import itertools
from psyrts.agents import Competitor, Predator, Participant, Resources, CentralPlace, BreadCrumb
from psyrts.schedule import RandomActivationByBreed

# Start of datacollector functions
def resourcesRatio(model):
    if model.resourcesParticipants == 0:
        return 0
    else:
        return  model.resourcesParticipants / model.resources

def exploration(model):
    return   (number_visited( model, True) )/328





def exploitation(model):

    return   ((number_visited( model, False) )/72) * resourcesRatio(model)


def number_visited(model ,mode_exploration=True):

    next_moves = []
    if mode_exploration:
        next_moves = model.locationsExploration
    else:
        next_moves = model.locationsExploitation
  # print( "size grid " + str(len(next_moves)))
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



def track_params(model):
    return (model.initial_competitors,
            model.initial_explorers,
            model.initial_predators,
            model.visibility)

def track_run(model):
    return model.schedule.steps

def track_experiment(model):
    return model.uid



class PsyRTSGame(Model):
    # id generator to track run number in batch run data
    id_gen = itertools.count(1)

    height = 20
    width = 20

    verbose = False  # Print-monitoring


    description = 'A model for simulating participants running the different experiments.'

    def __init__(self, height=20, width=20, visibility = False ,initial_competitors=1,
                 initial_explorers=1, initial_predators=1):
        '''
        Create a new PsyRTS  model with the given parameters.

        Args
            initial_competitors: Number of units each participant knows
            initial_explorers: Number of sheep to start with
            initial_predators: Number of wolves to start with
            visibility : total or partial visibility
        '''
        super().__init__()
        self.uid = next(self.id_gen)
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
        self.noise = 0.0
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
            model_reporters={
                "Experiment_Synth": track_experiment,
                "Conditions": track_params,
                "Step": track_run,
                "Exploration": exploration ,
                             "Exploitation": exploitation,
                              "ResourcesRatio": resourcesRatio
                             })   #reporto a datos

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
             irand = randrange(1, 11)
             #irand = 4
             #print("resource con valores {} ". format(  irand)  )
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


    def updateNoise(self):

        if self.visibility:
            self.noise = 0.4
        else:
            self.noise = 0.5

        self.noise = self.noise + (( .03)*self.schedule.get_breed_count(Competitor))
        self.noise = self.noise + ((.02) * self.schedule.get_breed_count(Predator))

    def step(self):

        self.datacollector.collect(self)
        self.schedule.step()
        self.updateNoise()
        # collect data

        participantsAlive = self.schedule.get_breed_count(Participant)
        if participantsAlive <=0:
            print("Stop Participants dead")
            self.running = False

        if self.resourcesCompetitors +self.resourcesParticipants == self.resources:
            print("Stop No More Resources")
            self.running = False

        if self.schedule.steps>150:
            print("toomany steps")
            self.running = False

    def run_model(self, step_count=150):
        for i in range(step_count):
            self.step()

