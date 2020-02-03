import numpy as np
from random import seed
from random import random, randint


class Grid:
    """ A class to represent simulation Grid """
    def __init__(self, rows, columns):
        self.grid = self.create_grid(columns, rows)

        self.businesses = []
        self.freeways = []
        self.education = []
        self.crime_centers = []

    """ GRID FEATURES -----------------------------------------------------------------------------------------------"""

    def make_freeway(self, rand, num_freeways):
        num_rows = self.get_num_rows()
        num_cols = self.get_num_cols()
        orientation = random.choice(["row", "column"])
        # list of gridsquares in the freeway
        freeway: GridSquare = []
        # column freeway
        if orientation.equals("column"):
            # freeway_length = rand.randint(num_rows - 1)
            # freeway_col = rand.randint(num_cols - 1)
            freeway_length = num_rows
            freeway_col = 0
            for i in range(freeway_length):
                freeway_square = self.get_grid_square(i, freeway_col)
                freeway_square.set_freeway(True)
                freeway.append(freeway_square)
        # row freeway
        else:
            # freeway_length = rand.randint(num_cols - 1)
            # freeway_row = rand.randint(num_rows - 1)
            freeway_length = num_cols
            freeway_row = 0
            for i in range(freeway_length):
                freeway_square = self.get_grid_square(i, freeway_row)
                freeway_square.set_freeway(True)
                freeway.append(freeway_square)

        self.freeways.append(freeway)
        return

    def make_businesses(self, rand, num_biz):
        """ Create a business in the following square """
        row = rand.randint(self.grid.get_num_rows())
        column = rand.randint(self.grid.get_num_cols())
        business = self.get_grid_square(row, column)
        business.set_business(True)
        self.businesses.append(business)

    def make_education(self, rand, num_education):
        """ Create a business in the following square """
        row = rand.randint(self.grid.get_num_rows())
        column = rand.randint(self.grid.get_num_cols())
        education = self.get_grid_square(row, column)
        education.set_education(True)
        self.education.append(education)

    """ GRID GETTERS ------------------------------------------------------------------------------------------------"""

    def get_size(self):
        return self.grid.shape

    def get_num_rows(self):
        return self.get_size()[0]

    def get_num_cols(self):
        return self.get_size()[1]

    def get_grid_square(self, r, c):
        return self.grid[r][c]

    def get_businesses(self):
        return self.businesses

    def get_freeways(self):
        return self.freeways

    def get_education(self):
        return self.education

    def create_grid(self, rows, columns):
        grid = np.array([[GridSquare(r, c,
            total_houses=10, occupied_houses=0, crime=10, education=10, business=True, freeway=True)
            for r in range(rows)] for c in range(columns)])
        return grid


    from person import Person
    def find_appropriate_housing(self, person: Person):
        max_sq = None
        max_i = -1
        max_j = -1
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                sq: GridSquare = self.grid[i][j]
                if sq.get_total_houses() - sq.get_occupied_houses() <= 0:
                    continue
                if sq.price < person.price_point:
                    if max_sq is None:
                        max_sq = sq
                        max_i = i
                        max_j = j
                    elif sq.price > max_sq.price:
                        max_sq = sq
                        max_i = i
                        max_j = j
        return max_sq, max_i, max_j


class GridSquare:
    """ A class to represent a single square in the simulation Grid
    A grid has a total number of houses, a number of occupied houses, and a list of houses
    """
    def __init__(self,  r, c, total_houses, occupied_houses, crime, education, business, freeway):
        self.total_houses = total_houses
        self.occupied_houses = occupied_houses
        self.price = self.sample_monthly_total_costs()
        self.crime = crime
        self.education = education
        self.business = business
        self.freeway = freeway

    """ Increment and decrement occupied houses """
    def movein(self):
        if self.occupied_houses < self.total_houses:
            self.occupied_houses += 1
            return "Moved in to a house"
        else:
            return "Could not move in to a house"

    def moveout(self):
        if self.occupied_houses > 0:
            self.occupied_houses -= 1
            return "Removed one occupied house"
        else:
            return "Could not move out of occupied house"

    """ GRID SQUARE GETTERS -----------------------------------------------------------------------------------------"""

    def get_total_houses(self):
        return self.total_houses
    def get_occupied_houses(self):
        return self.occupied_houses
    def get_price(self):
        return self.price
    def get_crime(self):
        return self.crime
    def get_education(self):
        return self.education
    def get_business(self):
        return self.business
    def get_freeway(self):
        return self.freeway

    """ GRID SQUARE SETTERS -----------------------------------------------------------------------------------------"""

    def set_education(self, boolean):
        self.education = boolean

    def set_business(self, boolean):
        self.business = boolean

    def set_freeway(self, boolean):
        self.freeway = boolean

    def set_crime(self, boolean):
        self.crime = boolean

    @staticmethod
    def sample_monthly_total_costs():
        from main import monthly_cost_data
        rn = randint(0, 100) / 100
        for i in range(len(monthly_cost_data) - 1, -1, -1):
            if monthly_cost_data[i][1] < rn:
                return monthly_cost_data[i][0]
        return 1

if __name__ == "__main__":
    my_grid = Grid(8, 8)
    print(my_grid.grid)
    for row in my_grid.grid:
        for col in row:
            print(col.get_price())


