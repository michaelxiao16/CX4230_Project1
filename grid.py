from typing import List

import numpy as np
from random import random, randint, choice
from person import Person
from bintrees import AVLTree
from feature_importance import get_feature_vector


def get_unique_key(gs, tree: AVLTree):
    """
    Many gridsquares will have the same price, so it's important to generate a unique key since the AVL library doesn't
    allow for duplicate keys
    :param gs: gridsquare
    :param tree: avl to check keys against
    :return: a unique key close to the price point p
    """
    p = gs.get_price()
    if p in tree:
        while p in tree:
            p -= 0.01
    gs.key = p
    return p


class Grid:
    """ A class to represent simulation Grid """

    def __init__(self, rows, columns):
        """
        Initialize grid. For every grid square, add it to the AVL, since when the grid is initialized, there are no
        people living in it, meaning every grid square should be in the tree of available units.
        :param rows:
        :param columns:
        """
        self.grid = self.create_grid(columns, rows)

        self.businesses = []
        self.freeways = []
        self.education_centers = []
        self.crime_centers = []
        self.tree = AVLTree()
        self.feature_coeffs = get_feature_vector()
        for row in self.grid:
            for gs in row:
                self.add_gs_to_tree(gs)

        self.grid_setup()

    """WRAPPER METHODS FOR CONTROLLING ACCESS TO THE TREE OF AVAILABLE GRIDSQUARES"""
    def add_gs_to_tree(self, gs):
        k = get_unique_key(gs, self.tree)
        self.tree[k] = gs
        gs.in_tree = True

    def remove_gs_from_tree(self, gs):
        del self.tree[gs.key]
        gs.in_tree = False

    """ GRID FEATURES -----------------------------------------------------------------------------------------------"""

    def make_freeway(self, num_freeways):
        num_rows = self.get_num_rows()
        num_cols = self.get_num_cols()
        businesses = self.get_businesses()
        f_business = choice(businesses)

        orientation = choice(["row", "column"])
        # list of gridsquares in the freeway
        freeway: GridSquare = []
        # column freeway
        if orientation == "column":
            freeway_length = num_rows
            freeway_col = f_business[0]
            for i in range(freeway_length):
                freeway_square = self.get_grid_square(i, freeway_col)
                freeway_square.set_freeway(True)
                freeway.append(freeway_square.get_location())
        # row freeway
        else:
            freeway_length = num_cols
            freeway_row = f_business[1]
            for i in range(freeway_length):
                freeway_square = self.get_grid_square(i, freeway_row)
                freeway_square.set_freeway(True)
                freeway.append(freeway_square.get_location())

        self.freeways.append(freeway)
        return

    def make_businesses(self, business_levels, business_locations):
        """ Create a business in the following square """

        for level, location in zip(business_levels, business_locations):
            row, column = location
            business = self.get_grid_square(row, column)
            business.set_business(level)
            self.businesses.append(business.get_location())

    def make_education_center(self, education_levels, education_centers):
        """ Create a business in the following square """
        for level, location in zip(education_levels, education_centers):
            row, column = location
            education = self.get_grid_square(row, column)
            education.set_education(level)
            self.education_centers.append(education.get_location())

    def create_grid(self, rows, columns):
        grid = np.array([[GridSquare(r, c,
                                     total_houses=10, occupied_houses=0, crime=[], education=[], business=[],
                                     freeway=True, grid=self)
                          for r in range(rows)] for c in range(columns)])
        return grid

    def grid_setup(self):

        # for e in range(randint(0,4)):
        business_levels = [0.9]
        business_locations = [(2, 1)]
        self.make_businesses(business_levels, business_locations)
        education_level = [0.8]
        education_centers = [(1, 5)]
        self.make_education_center(education_level, education_centers)

        self.make_freeway(1)

        return

    def update_grid_prices(self):
        from main import monthly_cost_data
        sqs = []
        for row in self.grid:
            for gs in row:
                feature_vec = gs.get_value_score()
                score = feature_vec @ self.feature_coeffs
                sqs.append((score, gs))
        sqs: List[(int, GridSquare)] = sorted(sqs, key=lambda x: x[0])
        total = len(sqs)
        monthly_cost_non_cum = []
        for i in range(len(monthly_cost_data) -1, -1, -1):
            if i != 0:
                monthly_cost_non_cum.insert(0, (monthly_cost_data[i][0], monthly_cost_data[i][1] - monthly_cost_data[i-1][1]))
            else:
                monthly_cost_non_cum.insert(0, (monthly_cost_data[i][0], monthly_cost_data[i][1]))
        for pair in monthly_cost_data:
            num = int(np.ceil(pair[1] * total))
            for _ in range(num):
                try:
                    sqs.pop(0)[1].set_price(pair[0])
                except IndexError as _:
                    continue
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

    def get_education_centers(self):
        return self.education_centers


    from person import Person

    def find_appropriate_housing(self, person: Person):
        """
        Assume an individual will buy a house within a certain bound of their price point, i.e. 20 percent. Index this
        range of keys from the AVL and pull out the last one, which maximizes the value of the houses. If this index is
        invalid, return None, -1, -1
        :param person: person to search avl for available housing
        :return: grid square that maximizes value or None, along with locations
        """
        valid_homes = self.tree[0:person.price_point*1.2]
        try:
            last = self.tree[list(valid_homes.keys())[-1]]
            r, c = last.location[0], last.location[1]
        except IndexError as _:
            last = None
            r, c = -1, -1
        return last, r, c


class GridSquare:
    """ A class to represent a single square in the simulation Grid
    A grid has a total number of houses, a number of occupied houses, and a list of houses. The grid-square also
    contains a list of pointers to every Person that lives in its square. Each gridsquare also contains a pointer to
    the overall parent grid (this is added for access to the AVL)
    """

    def __init__(self, r, c, total_houses, occupied_houses, crime, education, business, freeway, grid):
        self.row = r
        self.column = c
        self.total_houses = total_houses
        self.occupied_houses = occupied_houses
        self.price = self.sample_monthly_total_costs()
        self.crime = crime
        self.education = education
        self.business = business
        self.freeway = freeway
        self.threads: List[Person] = []
        self.location = (c, r)
        self.grid: Grid = grid
        self.key = -1
        self.in_tree = False

    """ Increment and decrement occupied houses """

    def movein(self, thread: Person):
        if self.occupied_houses < self.total_houses:
            self.occupied_houses += 1
            self.threads.append(thread)
            # If we have reached grid capacity, it should no longer be in the tree
            if self.occupied_houses == self.total_houses:
                self.grid.remove_gs_from_tree(self)
            return "Moved in to a house"
        else:
            return "Could not move in to a house"

    def moveout(self, thread: Person):
        if self.occupied_houses > 0:
            self.occupied_houses -= 1
            self.threads.remove(thread)
            # if a house has become available and we're not already in the tree, we should be added to it
            if not self.in_tree:
                self.grid.add_gs_to_tree(self)
            return "Removed one occupied house"
        else:
            return "Could not move out of occupied house"

    """ GRID SQUARE GETTERS -----------------------------------------------------------------------------------------"""
    def get_location(self):
         return (self.row, self.column)

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

    def get_value_score(self):
        my_grid = self.grid
        # Poor people, crime, distance to business center, education level, distance to nearest highway
        total_dist = 0
        for business in my_grid.get_businesses():
            total_dist += np.sum(np.abs(np.array(business) - np.array((self.row, self.column))))
        # Calculate average distance
        avg_dist = total_dist / len(my_grid.get_businesses())
        # Normalize avg dist
        norm_dist = avg_dist / (my_grid.get_num_rows() + my_grid.get_num_cols())
        dist_business = norm_dist

        total_education = 0
        for education in my_grid.get_education_centers():
            total_education += np.sum(np.abs(np.array(education) - np.array((self.row, self.column))))
        # Calculate average distance
        avg_education = total_education / len(my_grid.get_education_centers())
        # Normalize avg dist
        norm_education = avg_education / (my_grid.get_num_rows() + my_grid.get_num_cols())
        education_level = norm_education
        value = [0, 0, dist_business, education_level, 0]
        return np.array(value)


    """ GRID SQUARE SETTERS -----------------------------------------------------------------------------------------"""

    def set_education(self, education_level):
        self.education = education_level

    def set_business(self, business_level):
        self.business = business_level

    def set_freeway(self, boolean):
        self.freeway = boolean

    def set_crime(self, boolean):
        self.crime = boolean

    def set_price(self, price):
        self.price = price

    def get_average_income(self):
        """
        For every person living in this grid square, sum up their income and return the average. Mainly for use
        in gathering metrics at the beginning and end of the experiments.
        :return: average income for all Persons in this square
        """
        if len(self.threads) == 0:
            return 0
        agg = 0
        for t in self.threads:
            agg += t.get_income()
        return agg / len(self.threads)

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
    print(len(my_grid.tree))
    my_grid.update_grid_prices()
