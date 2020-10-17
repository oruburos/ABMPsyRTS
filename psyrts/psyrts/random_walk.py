'''
Generalized behavior for random walking, one grid cell at a time.
'''

from mesa import Agent


class RandomWalker(Agent):
    '''
    Class implementing random walker methods in a generalized manner.

    Not indended to be used on its own, but to inherit its methods to multiple
    other agents.

    '''

    grid = None
    x = None
    y = None
    moore = True

    def __init__(self, unique_id, pos, model, moore=True):
        '''
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        '''
        super().__init__(unique_id, model)
        self.pos = pos
        self.pos = pos
        self.moore = moore

    def random_move(self):
        '''
        Step one cell in any allowable direction.
        '''
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)

    def random_move_double(self):
        '''
        Step one cell in any allowable direction.
        '''
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        doublemove = []
        for moves in next_moves:
            doublemove.append( self.model.grid.get_neighborhood(moves,self.moore,True))

        next_move = self.random.choice(doublemove)
        # Now move:
        self.model.grid.move_agent(self, next_move)



    def move_towards(self, cosa):

        posactual = self.pos
        newx= 0
        newy = 0
        direction =cosa






        if posactual[0] == direction[0]: #same x

            newx = posactual[0]


            if posactual[1] < direction[1]:
                newy = posactual[1]+1
            elif posactual[1] > direction[1]:
                newy = posactual[1] - 1
            else:
                newy = posactual[1]

        elif posactual[0] < direction[0]: #
            newx = posactual[0] + 1
            if posactual[1] < direction[1]:
                newy = posactual[1] + 1

            elif posactual[1] > direction[1]:
                newy = posactual[1] - 1

            else:# =
                newy = posactual[1]

        else:
            newx = posactual[0] - 1
            if posactual[1] < direction[1]:
                newy = posactual[1] + 1
            elif posactual[1] > direction[1]:
                newy = posactual[1] - 1
            else:
                newy = posactual[1]

        if newx < 0:
            newx = 0
        if newy < 0:
            newy = 0

        if newy > 19:
            newy = 19
        if newx > 19:
            newx = 19

        next_move = (newx, newy)

        #print( "my pos " + str(self.pos) + " my goal " + str(direction) + " next move " + str(next_move))
        self.model.grid.move_agent(self, next_move)

    def move_away(self, cosa):

        posactual = self.pos
        newx= 0
        newy = 0
        direction = cosa
        if posactual[0] == direction[0]:
            if posactual[1] < direction[1]:
                newx =posactual[0] +1
                newy = posactual[1]-1
                if newy<0:
                    newy=0
                if newx>19:
                    newx=19
            else:
                newx = posactual[0] +1
                newy = posactual[1] + 1
                if newx>19:
                    newx=19
                if newy>19:
                    newy=19
        elif posactual[0] < direction[0]:
            if posactual[1] < direction[1]:
                newx = posactual[0] -1
                newy = posactual[1] - 1

                if newx<0:
                   newx=0
                if newy < 0:
                   newy = 0
            else:
                newx = posactual[0] -1
                newy = posactual[1] + 1

                if newx<0:
                    newx=0
                if newy > 19:
                   newy = 19


        else:
            if posactual[1] < direction[1]:
                newx = posactual[0] +1
                newy = posactual[1] - 1
                if newx > 19:
                    newx = 19
                if newy < 0:
                   newy = 0
            else:

                newx = posactual[0] +1
                newy = posactual[1] + 1

                if newx > 19:
                    newx = 19
                if newy > 19:
                    newy = 19

        next_move = (newx, newy)

       # print( "my pos " + str(self.pos) + " my goal " + str(direction) + " next move " + str(next_move))
        self.model.grid.move_agent(self, next_move)

