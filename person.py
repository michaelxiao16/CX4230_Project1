from threading import Thread, Condition
from typing import Tuple
import random


class Person(Thread):
    """ A class to represent people in simulation """
    from event import Event

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

    def run(self):
        from main import grid
        event = self.next_event
        if event.type == 0:
            self.gl.cv_time.acquire()
            while self.gl.clock < self.next_event.time_stamp:
                self.gl.cv_time.wait()
            # event.function()
            self.move_out_event()
            self.next_event = None
            self.gl.cv_time.release()
        else:
            self.gl.cv_housing.acquire()
            while grid.find_appropriate_housing(self)[0] is None:
                self.gl.cv_housing.wait()
            sq, i, j = grid.find_appropriate_housing(self)
            # event.function(i, j)
            self.move_in_event(i, j)
            self.next_event = None
            self.gl.cv_housing.release()

    def move_out_event(self):
        from main import grid, Event
        from grid import GridSquare
        sq: GridSquare = grid.get_grid_square(self.home_location[0], self.home_location[1])
        loc = self.home_location
        self.home_location = (-1, -1)
        sq.moveout()
        event = Event(-1, self.pid, self.move_in_event, True, 1)
        self.schedule_event(event)
        self.gl.cv_housing.acquire()
        self.gl.cv_housing.notifyAll()
        self.gl.cv_housing.release()
        print("moved out of " + str(loc[0]) + ' ' + str(loc[1]))

    def move_in_event(self, row, col):
        from main import grid, move_out_data, Event
        from grid import GridSquare
        self.home_location = (row, col)
        loc = self.home_location
        sq: GridSquare = grid.get_grid_square(self.home_location[0], self.home_location[1])
        sq.movein()
        rn = random.randint(0, 100) / 100
        years = 0
        for i in range(len(move_out_data) - 1, -1, -1):
            if move_out_data[i] < rn:
                years = i + 1
                break
        t = self.gl.clock + years
        event = Event(t, self.pid, self.move_out_event, True, 0)
        self.schedule_event(event)
        print("moved into " + str(loc[0]) + ' ' + str(loc[1]))

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
        self.gl.queue_lock.acquire()
        if event_i.type == 0:
            # fel.put(event_i)
            heappush(self.gl.fel, event_i)
        else:
            self.gl.wait_list.insert(0, event_i)
        self.gl.queue_lock.release()
