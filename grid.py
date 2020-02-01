import numpy as np
class Grid:
    """ A class to represent simulation Grid """


    def get_grid_square(self, r, c):
        return

    def create_grid(self, rows, columns):
        grid = np.zeros(shape=(rows, columns))
        return grid
    def __init__(self, rows, columns):
        self.create_grid(columns, rows)

class GridSquare:
    """ A class to represent a single square in the simulation Grid"""
    def __init__(self, total_houses, occupied_houses):
        self.total_houses = total_houses
        self.occupied_houses = occupied_houses