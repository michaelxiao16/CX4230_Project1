""" Import statements """
from heapq import heappush, heappop
from typing import List

import numpy as np
import random

import grid_view
from event import Event
from grid import Grid
from prob_distributions import get_salary_prob, get_move_out_prob, get_monthly_total_costs_prob, \
    get_percent_monthly_income

GRID_ROWS = 10
GRID_COLS = 10
NUM_RUNS = 10000
NUM_THREADS = GRID_COLS * GRID_ROWS * 10


class Globals:
    """Class to contain all the global variables that are passed to individual threads"""
    def __init__(self, fel_i, waiting_list_i, clock, threads, grid):
        """
        :param fel_i: Future event list. Contains timestamp based events
        :param waiting_list_i: Waiting list. Contains all events waiting on predicates.
        :param clock: Global simulation time
        :param threads:
        :param grid:
        """
        self.fel = fel_i
        self.wait_list = waiting_list_i
        self.clock = clock
        self.threads = threads
        self.grid = grid


""" STATIC variables """
# Define all probability distributions
salary_data = get_salary_prob()
move_out_data = get_move_out_prob()
monthly_cost_data = get_monthly_total_costs_prob()
percent_monthly_income_data = get_percent_monthly_income()


def schedule_event(event_i: Event, gl: Globals):
    """
    Put event into future event list. Only called for starting the simulation
    :param gl: global variables object
    :param event_i: event to schedule
    """
    heappush(gl.fel, event_i)
    gl.threads[event_i.process_id].next_event = event_i


def assign_first_available_house(person_i, first_house, gl: Globals):
    from grid import GridSquare
    """
    Assign this person to the first available house
    :param first_house: optimization parameter to speed up initial assignment by not checking houses already assigned
    :param person_i: thread to be assigned to house
    :return True if the assignment was successful, false otherwise
    """
    for m in range(first_house[0], gl.grid.grid.shape[0]):
        for k in range(gl.grid.grid.shape[1]):
            grid_square: GridSquare = gl.grid.grid[m][k]
            if grid_square.get_total_houses() - grid_square.get_occupied_houses() > 0:
                grid_square.movein(person_i)
                person_i.home_location = (m, k)
                pair = (m, k)
                if grid_square.get_total_houses() - grid_square.get_occupied_houses() == 0:
                    if k == GRID_COLS:
                        pair = (m + 1, 0)
                return True, pair
    return False, first_house


def initialize_persons(gl: Globals, num_threads=20000):
    """
    Instantiates num_threads amount of Person objects with "random" housing and schedules move out events for them
    Important note: the assigning of individuals may fail. In this case individuals who cannot afford any houses that
    remain will be assigned to location (-1, -1), and they will be put on the waiting list with a move in event
    scheduled.
    :param gl: global variables object
    :param num_threads: amount of Persons to generate
    """
    # first house is the optimization parameter. It keeps track of where we are in the array so we don't have to check
    # places we've already assigned
    from person import Person
    first_house = (0, 0)
    for ii in range(num_threads):
        gl.threads.append(Person(None, ii, (-1, -1), gl))
        assigned, first_house = assign_first_available_house(gl.threads[ii], first_house, gl)
        if assigned:
            years = Person.sample_move_out_distribution(0)
            t_i = gl.clock + years
            event_i = Event(t_i, ii, Person.move_out_event, True, 0)
            schedule_event(event_i, gl)
        else:
            schedule_event(Event(gl.clock + random.randint(0, 2), ii, Person.move_in_event, True, 1), gl)
        gl.threads[ii].next_event = None
        gl.threads[ii].start()
    ts = sorted(gl.threads, key=lambda x: x.income)
    for help_i in range(int(NUM_THREADS * 0.12)):
        ts[help_i].price_point += 600


def sim_snapshot(counter_i, graph_data, gl: Globals, frequency=600):
    """
    Take a data snapshot of the simulation if the mod of the counter and the frequency is zero
    :param gl: global variables object
    :param graph_data: array for visualization in grid_view
    :param counter_i: current iteration of simulation run
    :param frequency: how often to take a snapshot
    """
    if counter_i % frequency == 0:
        arr_num_people = np.zeros((GRID_ROWS, GRID_COLS))
        arr_money = np.zeros((GRID_ROWS, GRID_COLS))
        for person_i in gl.threads:
            if person_i.home_location[0] != -1:
                loc = person_i.home_location
                arr_money[loc[0]][loc[1]] = person_i.income
        for ri in range(GRID_ROWS):
            for rj in range(GRID_COLS):
                arr_num_people[ri, rj] = gl.grid.get_grid_square(ri, rj).get_occupied_houses()
        graph_data.append((arr_money, arr_num_people))


def get_average_disparity(gl: Globals):
    """
    Function to return average disparity among all squares on the grid. The average income from the square is compared
    with that of all of its immediate neighbors. Some index checking is performed to ensure that there is no indexing
    out of bounds
    :return: average difference in income between a square and its neighbors
    """
    from grid import GridSquare
    aggregate = 0
    count = 0
    max_row, max_col = gl.grid.grid.shape
    for iii in range(max_row):
        for jjj in range(max_col):
            neighbors: List[GridSquare] = []
            if iii > 0 and len(gl.grid.get_grid_square(iii-1, jjj).threads) != 0:
                neighbors.append(gl.grid.get_grid_square(iii - 1, jjj))
            if jjj > 0 and len(gl.grid.get_grid_square(iii, jjj-1).threads) != 0:
                neighbors.append(gl.grid.get_grid_square(iii, jjj - 1))
            if iii < max_row - 1 and len(gl.grid.get_grid_square(iii+1, jjj).threads) != 0:
                neighbors.append(gl.grid.get_grid_square(iii + 1, jjj))
            if jjj < max_col - 1 and len(gl.grid.get_grid_square(iii, jjj + 1).threads) != 0:
                neighbors.append(gl.grid.get_grid_square(iii, jjj + 1))

            sq_d: GridSquare = gl.grid.get_grid_square(iii, jjj)
            agg_local = 0
            for n in neighbors:
                agg_local += np.abs((sq_d.get_average_income() - n.get_average_income()))
            if len(neighbors) != 0:
                agg_local /= len(neighbors)
            aggregate += agg_local
            count += 1
    return aggregate/count


def main_sim_loop():
    from person import Person
    gl = Globals([], [], 0, [], Grid(GRID_ROWS, GRID_COLS))
    graph_data = []
    initialize_persons(gl, num_threads=NUM_THREADS)
    # print the starting average disparity
    print(get_average_disparity(gl))
    counter = 0
    disparities = [(0, get_average_disparity(gl))]
    while counter < NUM_RUNS:
        if counter % 100 == 0:
            gl.grid.update_grid_prices()
        # if the clock has gone up a year, get a disparity reading
        if disparities[-1][0] != gl.clock:
            disparities += [(gl.clock, get_average_disparity(gl))]
        # Attempt to record a snapshot of the simulation
        sim_snapshot(counter, graph_data, gl)
        try:
            event: Event or None = heappop(gl.fel)
        except IndexError as _:
            event = None
        # If there are still events in the future event list
        if event is not None:
            # Threaded events (Person)
            if event.is_thread and event.type == 0:
                gl.clock = event.time_stamp
                person: Person = gl.threads[event.process_id]
                person.next_event = event
                person.run()
                # Wait for thread to finish to ensure there is no concurrency
                person.join()
            elif event.is_thread and event.type == 1:
                gl.wait_list.append(event)
        # Loop through the Persons waiting on the waiting list. Check their predicate. If true, run the event
        for i in range(len(gl.wait_list) - 1, -1, -1):
            event = gl.wait_list[i]
            sq, _, _ = gl.grid.find_appropriate_housing(gl.threads[event.process_id])
            if sq is not None:
                del gl.wait_list[i]
                t = gl.threads[event.process_id]
                t.next_event = event
                t.run()
                t.join()

        counter += 1
    # print the ending average disparity
    print(get_average_disparity(gl))
    print(gl.clock)
    print(disparities)
    grid_view.plot_warm_up(disparities)
    grid_view.main(graph_data, gl.grid)


if __name__ == "__main__":
    # import statements to avoid circular imports
    main_sim_loop()
