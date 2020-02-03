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

    def __init__(self, cv_time: Condition, cv_housing: Condition,
                 next_event: Event, pid: int, home_location: Tuple[int, int]):
        super().__init__()
        self.income = self.sample_salary_distribution()
        self.price_point = (self.income * self.sample_percent_monthly_income())/12
        self.cv_time = cv_time
        self.cv_housing = cv_housing
        self.next_event = next_event
        self.pid = pid
        self.home_location = home_location

    def run(self):
        from main import clock, grid
        event = self.next_event
        cv = event.cv
        cv.acquire()
        if cv == self.cv_time:
            while clock < self.next_event.time_stamp:
                cv.wait()
            event.function()
            self.next_event = None
            cv.release()
        else:
            while grid.find_appropriate_housing(self) is None:
                cv.wait()
            sq, i, j = grid.find_appropriate_housing(self)
            event.function(self, row=i, col=j)
            self.next_event = None
            cv.release()

    def move_out_event(self):
        from main import grid, Event, schedule_event
        from grid import GridSquare
        sq: GridSquare = grid.get_grid_square(self.home_location[0], self.home_location[1])
        loc = self.home_location
        self.home_location = (-1, -1)
        sq.moveout()
        event = Event(-1, self.pid, self.move_in_event, True, self.cv_housing)
        schedule_event(event)
        print("moved out of " + str(loc[0]) + ' ' + str(loc[1]))

    def move_in_event(self, row, col):
        from main import grid, move_out_data, Event, clock, schedule_event
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
        t = clock + years
        event = Event(t, self.pid, self.move_out_event, True, self.cv_time)
        schedule_event(event)
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
