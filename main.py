""" Import statements """
import random
from heapq import heappush, heappop
import numpy as np

import grid_view
from event import Event
from grid import Grid
from prob_distributions import get_salary_prob, get_move_out_prob, get_monthly_total_costs_prob,\
    get_percent_monthly_income

GRID_ROWS = 10
GRID_COLS = 10
NUM_RUNS = 1200


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


# Define all probability distributions
salary_data = get_salary_prob()
move_out_data = get_move_out_prob()
monthly_cost_data = get_monthly_total_costs_prob()
percent_monthly_income_data = get_percent_monthly_income()

# Instantiate globals
gl = Globals([], [], 0, [], Grid(GRID_ROWS, GRID_COLS))


def schedule_event(event_i: Event):
    """
    Put event into future event list. Only called for starting the simulation
    :param event_i: event to schedule
    """
    heappush(gl.fel, event_i)
    gl.threads[event_i.process_id].next_event = event_i


def assign_first_available_house(person_i):
    """
    Assign this person to the first available house
    :param person_i: thread to be assigned to house
    """
    for m in range(gl.grid.grid.shape[0]):
        for k in range(gl.grid.grid.shape[1]):
            grid_square: GridSquare = gl.grid.grid[m][k]
            if grid_square.get_total_houses() - grid_square.get_occupied_houses() > 0:
                grid_square.movein()
                person_i.home_location = (m, k)
                return


def initialize_persons(num_threads=2000):
    """
    Instantiates num_threads amount of Person objects with "random" housing and schedules move out events for them
    :param num_threads: amount of Persons to generate
    """
    for ii in range(num_threads):
        gl.threads.append(Person(None, ii, (-1, -1), gl))
        years = Person.sample_move_out_distribution(0)
        t_i = gl.clock + years
        event_i = Event(t_i, ii, Person.move_out_event, True, 0)
        schedule_event(event_i)
        gl.threads[ii].next_event = None
        assign_first_available_house(gl.threads[ii])
        gl.threads[ii].start()


def sim_snapshot(counter_i, frequency=10):
    """
    Take a data snapshot of the simulation if the mod of the counter and the frequency is zero
    :param counter_i: current iteration of simulation run
    :param frequency: how often to take a snapshot
    """
    if counter_i % frequency == 0:
        arr = np.zeros((GRID_ROWS, GRID_COLS))
        for person_i in gl.threads:
            if person_i.home_location[0] != -1:
                loc = person_i.home_location
                arr[loc[0]][loc[1]] = person_i.income
        graph_data.append(arr)


if __name__ == "__main__":
    # import statements to avoid circular imports
    from person import Person
    from grid import GridSquare
    graph_data = []
    initialize_persons()
    counter = 0
    while counter < NUM_RUNS:
        # Attempt to record a snapshot of the simulation
        sim_snapshot(counter)
        try:
            event: Event or None = heappop(gl.fel)
        except IndexError as e:
            event = None
        # If there are still events in the future event list
        if event is not None:
            # Threaded events (Person)
            if event.is_thread and event.type == 0:
                gl.clock = event.time_stamp
                person: Person = gl.threads[event.process_id]
                person.next_event = event
                loc1 = person.home_location
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
    grid_view.main(graph_data)

