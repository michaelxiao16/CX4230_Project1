import numpy as np
from random import seed
from random import random
class Grid:
    """ A class to represent simulation Grid """
    def __init__(self, rows, columns):
        seed(16)
        highway_col = random()
        self.grid = self.create_grid(columns, rows)
        self.businesses = []
        self.freeways = []
        self.education = []

    def make_freeway(self, f_rand):
        num_rows = self.get_num_rows()
        num_cols = self.get_num_cols()
        orientation = random.choice(["row", "column"])


        # column freeway
        if orientation.equals("column"):
            # freeway_length = f_rand.randint(num_rows - 1)
            # freeway_col = f_rand.randint(num_cols - 1)
            freeway_length = num_rows
            freeway_col = 0

            for i in range(freeway_length):
                freeway_square = self.get_grid_square(i, freeway_col)
        # row freeway
        else:
            # freeway_row = f_rand.randint(num_rows - 1)
            freeway_length = num_cols
            freeway_row = 0

            for i in range(freeway_length):
                freeway_square = self.get_grid_square(i, freeway_row)
                freeway_square

        return

    def make_businesses(self, b_rand, num_biz):
        """ Create a business in the following square """
        row = b_rand.randint(self.grid.get_num_rows)
        column = b_rand.randint(self.grid.get_num_cols)
        business = 
        self.businesses.append()

    def get_size(self):
        return self.grid.shape

    def get_num_rows(self):
        return self.get_size()[0]

    def get_num_cols(self):
        return self.get_size()[1]


    def get_grid_square(self, r, c):
        return self.grid[r][c]

    def create_grid(self, rows, columns):
        grid = np.array([[GridSquare(r, c,
            houses = 10, total_houses = 10, occupied_houses = 10, crime = 10, education = 10, business = True, freeway = True)
            for r in range(rows)] for c in range(columns)])
        return grid

    def find_appropriate_housing(self):
        pass






class GridSquare:
    """ A class to represent a single square in the simulation Grid
    A grid has a total number of houses, a number of occupied houses, and a list of houses
    """
    def __init__(self,  r, c, houses, total_houses, occupied_houses, crime, education, business, freeway):
        self.total_houses = total_houses
        self.occupied_houses = occupied_houses
        self.houses = houses
        self.crime = crime
        self.education = education
        self.business = business
        self.freeway = freeway

    def get_crime(self):
        return self.crime
    def get_education(self):
        return self.education
    def get_business(self):
        return self.business

    def set_freeway(self):
        self.freeway = True





if __name__ == "__main__":
    my_grid = Grid(8, 8)
    print(my_grid.get_num_cols())


