""" Import statements """
# from queue import PriorityQueue
import random
from heapq import heappush, heappop
from threading import Condition, Lock
import numpy as np

import grid_view
from event import Event
from grid import Grid
from prob_distributions import get_salary_prob, get_move_out_prob, get_monthly_total_costs_prob,\
    get_percent_monthly_income


class Globals:
    def __init__(self, fel_i, waiting_list_i, clock, cv_housing, cv_time, queue_lock, threads):
        self.fel = fel_i
        self.wait_list = waiting_list_i
        self.clock = clock
        self.cv_housing = cv_housing
        self.cv_time = cv_time
        self.queue_lock = queue_lock
        self.threads = threads

# fel = PriorityQueue()
gl = Globals([], [], 0, Condition(Lock()), Condition(Lock()), Lock(), [])
salary_data = get_salary_prob()
move_out_data = get_move_out_prob()
monthly_cost_data = get_monthly_total_costs_prob()
percent_monthly_income_data = get_percent_monthly_income()
grid = Grid(10, 10)


def schedule_event(event_i: Event):
    heappush(gl.fel, event_i)
    gl.threads[event_i.process_id].next_event = event_i



def assign_random_house(person_i):
    for l in range(grid.grid.shape[0]):
        for k in range(grid.grid.shape[1]):
            grid_square: GridSquare = grid.grid[l][k]
            if grid_square.get_total_houses() - grid_square.get_occupied_houses() > 0:
                grid_square.movein()
                person_i.home_location = (l, k)
                return


if __name__ == "__main__":
    # Calls to setup grid and instantiate threads
    from person import Person
    from grid import GridSquare

    graph_data = []

    for i in range(100):
        gl.threads.append(Person(None, i, (-1, -1), gl))
        rn = random.randint(0, 100) / 100
        years = 0
        for j in range(len(move_out_data) - 1, -1, -1):
            if move_out_data[j] < rn:
                years = i + 1
                break
        t = gl.clock + years
        event = Event(t, i, Person.move_out_event, True, 0)
        schedule_event(event)
        gl.threads[i].next_event = event
        assign_random_house(gl.threads[i])
        gl.threads[i].start()

    counter = 0
    while counter < 1000:

        if counter % 10 == 0:
            arr = np.zeros((100, 100))
            for person in gl.threads:
                if person.home_location[0] != -1:
                    loc = person.home_location
                    arr[loc[0]][loc[1]] = person.income
            graph_data.append(arr)

        # event = fel.get_nowait()
        try:
            event: Event = heappop(gl.fel)
        except IndexError as e:
            event = None
        if event is not None:
            # Threaded events (Person)
            if event.is_thread and event.type == 0:
                gl.clock = event.time_stamp
                person: Person = gl.threads[event.process_id]
                person.resume()
            elif event.is_thread and event.type == 1:
                gl.wait_list.append(event)

        for i in range(len(gl.wait_list) - 1, -1, -1):
            event = gl.wait_list[i]
            sq, i, j = grid.find_appropriate_housing(gl.threads[event.process_id])
            if sq is not None:
                t = gl.threads[event.process_id]
                t.resume()
                del gl.wait_list[i]

        counter += 1
        print(counter)
    grid_view.main(graph_data)
