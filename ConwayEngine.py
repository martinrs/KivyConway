class World():

    def __init__(self, width, height):
        self.grid = Grid(width, height)
        self.generations = 0

    def flip(self):
        pass

    def randomize(self):
        pass

    def reset(self):
        pass

    def countLiveNeighbours(self, x, y):
        pass

    def update(self):
        pass

    def getDimensions(self):
        pass

class Grid():

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.cells = {}

    def update(self, newCells):
        pass

class Cell:

    def __init__(self, alive=False):
        self.isAlive = alive

    def toggleAlive(self):
        pass
