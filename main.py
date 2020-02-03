""" Import statements """
# from queue import PriorityQueue
from heapq import heappush, heappop
from threading import Condition, Lock

from event import Event
from grid import Grid
from prob_distributions import get_salary_prob, get_move_out_prob, get_monthly_total_costs_prob,\
    get_percent_monthly_income


class Globals:
    def __init__(self, fel_i, waiting_list_i, clock, cv_housing, cv_time, queue_lock):
        self.fel = fel_i
        self.wait_list = waiting_list_i
        self.clock = clock
        self.cv_housing = cv_housing
        self.cv_time = cv_time
        self.queue_lock = queue_lock


# fel = PriorityQueue()
gl = Globals([], [], 0, Condition(Lock()), Condition(Lock()), Lock())
salary_data = get_salary_prob()
move_out_data = get_move_out_prob()
monthly_cost_data = get_monthly_total_costs_prob()
percent_monthly_income_data = get_percent_monthly_income()
threads: list = []
grid = Grid(10, 10)


def schedule_event(event_i: Event):
    gl.queue_lock.acquire()
    if event_i.type == 0:
        # fel.put(event_i)
        heappush(gl.fel, event_i)
    else:
        gl.wait_list.append(event_i)
    gl.queue_lock.release()


if __name__ == "__main__":
    # Calls to setup grid and instantiate threads
    from person import Person
    for i in range(1001):
        threads.append(Person(None, i, (-1, -1), gl))
        event = Event(-1, i, Person.move_in_event, True, 1)
        threads[i].next_event = event
        threads[i].start()
    counter = 0
    while not len(gl.fel) == 0 or not len(gl.wait_list) == 0:
        # event = fel.get_nowait()
        try:
            event = heappop(gl.fel)
        except IndexError as e:
            event = None
        if event is not None:
            if event.is_thread:
                gl.clock = event.time_stamp
                threads[event.process_id].next_event = event
                threads[event.process_id].run()
            # gl.cv_time.acquire()
            # gl.cv_time.notify()
            # gl.cv_time.release()
        # if event.cv is not None:
        #     event.cv.release()
        # counter = 0
        for i in range(len(gl.wait_list) - 1, -1, -1):
            event = gl.wait_list[i]
            # event.cv.acquire()
            threads[event.process_id].next_event = event
            threads[event.process_id].run()
            del gl.wait_list[i]
            # counter += 1
            # print(counter)

            # event.cv.release()
        counter += 1
        print(counter)
