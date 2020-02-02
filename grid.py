import numpy as np
from random import seed
from random import random
class Grid:
    """ A class to represent simulation Grid """


    def make_freeway(self):
        return

    def get_grid_square(self, r, c):
        return

    def create_grid(self, rows, columns):
        grid = np.array([[GridSquare(10, 10, r, c) for r in range(rows)] for c in range(columns)])
        return grid
    def find_appropriate_housing(self):
        pass
    
    def __init__(self, rows, columns):
        seed(16)
        highway_col = random()


        self.create_grid(columns, rows)



class GridSquare:
    """ A class to represent a single square in the simulation Grid
    A grid has a total number of houses, a number of occupied houses, and a list of houses
    """
    def __init__(self, total_houses, occupied_houses, houses, r, c):
        self.total_houses = total_houses
        self.occupied_houses = occupied_houses
        self.houses = houses

    def get_crime(self):
        return self.crime


if __name__ == "__main__":
    my_grid = Grid(8, 8)


