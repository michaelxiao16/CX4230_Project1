""" Import statements """
# from queue import PriorityQueue
from heapq import heappush, heappop
from threading import Condition

from event import Event
from grid import Grid
from prob_distributions import get_salary_prob, get_move_out_prob, get_monthly_total_costs_prob,\
    get_percent_monthly_income

clock = 0
# fel = PriorityQueue()
fel = []
wait_list = []
salary_data = get_salary_prob()
move_out_data = get_move_out_prob()
monthly_cost_data = get_monthly_total_costs_prob()
percent_monthly_income_data = get_percent_monthly_income()
threads: list = []
grid = Grid(10, 10)
cv_time = Condition()
cv_housing = Condition()



def schedule_event(event_i: Event):
    if event_i.cv == cv_time:
        # fel.put(event_i)
        heappush(fel, event_i)
    else:
        wait_list.append(event_i)


if __name__ == "__main__":
    # Calls to setup grid and instantiate threads
    from person import Person
    for i in range(800):
        threads.append(Person(cv_time, cv_housing, None, i, (-1, -1)))
        event = Event(-1, i, Person.move_in_event, True, cv_housing)
        schedule_event(event)
    while not len(fel) == 0 or not len(wait_list) == 0:
        # event = fel.get_nowait()
        try:
            event = heappop(fel)
        except IndexError as e:
            event = None
        if event is not None:
            clock = event.time_stamp
            # if event.cv is not None:
            #     event.cv.acquire()
            if event.is_thread:
                threads[event.process_id].next_event = event
                threads[event.process_id].run()
        # if event.cv is not None:
        #     event.cv.release()
        for event in wait_list:
            # event.cv.acquire()
            threads[event.process_id].next_event = event
            threads[event.process_id].run()
            # event.cv.release()
        cv_housing.acquire()
        cv_housing.notifyAll()
        cv_housing.release()
        cv_time.acquire()
        cv_time.notifyAll()
        cv_time.release()
