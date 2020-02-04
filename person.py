from threading import Thread, Condition, Lock
from typing import Tuple
import random


class Person(Thread):
    """ A class to represent people in simulation """
    from event import Event

    """ GETTERS -----------------------------------------------------------------------------------------------------"""
    def get_income(self):
        return self.income

    def get_price_point(self):
        return self.price_point

    def __init__(self, next_event: Event, pid: int, home_location: Tuple[int, int], gl):
        super().__init__()
        self.income = self.sample_salary_distribution()
        self.price_point = (self.income * self.sample_percent_monthly_income())/12
        self.next_event = next_event
        self.pid = pid
        self.home_location = home_location
        self.gl = gl
        self.cond = Condition(Lock())
        self.paused = True
        self.cond.acquire()

    def pause(self):
        self.paused = True
        self.cond.acquire()

    def resume(self):
        self.paused = False
        self.cond.notify()
        self.cond.release()

    def run(self):
        # A person loops continuously between moving in and moving out
        event = self.next_event
        if event is None:
            return
        # Time based event: Someone is moving in, then schedule a move out event
        if event.type == 0:
            self.move_out_event()
        # Housing based event: wait for house to open up, then schedule a move out event
        elif event.type == 1:
            sq, i, j = self.gl.grid.find_appropriate_housing(self)
            if sq is None:
                return
            self.move_in_event(i, j)

    def move_out_event(self):
        from main import Event
        from grid import GridSquare
        sq: GridSquare = self.gl.grid.get_grid_square(self.home_location[0], self.home_location[1])
        loc = self.home_location
        self.home_location = (-1, -1)
        sq.moveout()
        event = Event(self.gl.clock + random.randint(0, 15), self.pid, self.move_in_event, True, 1)
        print("moved out of " + str(loc[0]) + ' ' + str(loc[1]))
        self.schedule_event(event)

    def move_in_event(self, row, col):
        from main import move_out_data, Event
        from grid import GridSquare
        self.home_location = (row, col)
        loc = self.home_location
        sq: GridSquare = self.gl.grid.get_grid_square(self.home_location[0], self.home_location[1])
        sq.movein()
        rn = random.randint(0, 100) / 100
        years = 0
        for i in range(len(move_out_data) - 1, -1, -1):
            if move_out_data[i] < rn:
                years = i + 1
                break
        t = self.gl.clock + years
        event = Event(t, self.pid, self.move_out_event, True, 0)
        print("moved into " + str(loc[0]) + ' ' + str(loc[1]))
        self.schedule_event(event)

    @staticmethod
    def sample_salary_distribution():
        from main import salary_data
        rn = random.randint(0, 100) / 100
        for i in range(len(salary_data) - 1, -1, -1):
            if salary_data[i][1] < rn:
                return salary_data[i][0]
        return 300000

    @staticmethod
    def sample_percent_monthly_income():
        from main import percent_monthly_income_data
        rn = random.randint(0, 100) / 100
        for i in range(len(percent_monthly_income_data) - 1, -1, -1):
            if percent_monthly_income_data[i][1] < rn:
                return percent_monthly_income_data[i][0]
        return 1


    def schedule_event(self, event_i: Event):
        from main import heappush
        self.next_event = event_i
        heappush(self.gl.fel, event_i)

