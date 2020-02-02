""" Import statements """
from queue import PriorityQueue
from threading import Condition
from person import Person
from typing import List

clock = 0
fel = PriorityQueue()
wait_list = []
threads: List[Person] = []


class Event:

    def __init__(self, t: float, pid: int, fun: classmethod, is_thread: bool,
                 cv: Condition):
        self.time_stamp = t
        self.process_id = pid
        self.function = fun
        self.is_thread = is_thread
        self.cv = cv


if __name__ == "__main__":
    # Calls to setup grid and instantiate threads

    cv_time = Condition()
    cv_housing = Condition()
    while not fel.qsize() == 0:
        event: Event = fel.get()
        clock = event.time_stamp
        if event.cv is not None:
            event.cv.acquire()
        if event.is_thread:
            threads[event.process_id].run()
        if event.cv is not None:
            event.cv.release()
        cv_time.notifyAll()
        cv_housing.notifyAll()
