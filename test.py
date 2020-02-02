from threading import Condition
from threading import Thread
import random

""" This class was created to demonstrate the raw functionality of the simulation
engine. """
clock = 0
events = []

class Event:

    def __init__(self, t: float, pid: int, fun: classmethod, is_thread: bool):
        self.time_stamp = t
        self.process_id = pid
        self.function = fun
        self.is_thread = is_thread

class ExampleThread(Thread):

    def __init__(self, i, cv):
        super().__init__()
        self.num = i
        self.cv = cv
        self.next_event = 0

    def run(self):
        cv.acquire()
        while clock < self.next_event:
            cv.wait()
        print(self.num, self.next_event)
        self.next_event = None
        cv.release()

    def schedule(self):
        random_num = random.randint(0, 9) + clock
        events.append({"t_num": self.num, "time_stamp": random_num})
        if self.next_event is None:
            self.next_event = random_num

if __name__ == '__main__':
    cv = Condition()
    a = ExampleThread.run
    threads = []
    for i in range(10):
        threads.append(ExampleThread(i, cv))
        rand_number = random.randint(0,9)
        threads[i].next_event = rand_number
        events.append({"t_num": i, "time_stamp": rand_number})
    events = sorted(events, key=lambda x: x["time_stamp"])
    events.reverse()
    while not len(events) == 0:
        event = events.pop()
        clock = event["time_stamp"]
        threads[event["t_num"]].run()
        cv.acquire()
        cv.notifyAll()
        cv.release()

