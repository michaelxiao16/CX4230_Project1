from threading import Thread
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
        """
        Initialize a person. Sample from various distributions to set starting points for various parameters
        :param next_event: the next event the person will run
        :param pid: id of the thread the Person will run on
        :param home_location: Location of the home initially assigned to the person
        :param gl: global variables pointed to by all threads. These variables are thread-safe.
        """
        super().__init__()
        self.income = self.sample_salary_distribution()
        self.price_point = (self.income * self.sample_percent_monthly_income())/12
        self.next_event = next_event
        self.pid = pid
        self.home_location = home_location
        self.gl = gl

    def run(self):
        """
        Tries to run the person loop. The event will be one of two types. If type 0, it's always run (first to pop off
        the future event list). Otherwise, we check for available appropriate housing. If there is none, return without
        doing anything.
        """
        from main import Event
        event = self.next_event
        # Important for when the people are initialized with no future events
        if event is None:
            return
        # Time based event: Someone is moving out. Call move_out_event, which schedules a move_in event
        if event.type == 0:
            self.move_out_event()
        # Housing based event: wait for house to open up, then schedule a move out event after moving in
        elif event.type == 1:
            sq, i, j = self.gl.grid.find_appropriate_housing(self)
            if sq is None:
                # the event has already been popped from the future event list. Put it back. This is mostly a failsafe
                # mechanism for threading as there SHOULD be no concurrency.
                self.schedule_event(Event(self.gl.clock + random.randint(0, 15), self.pid, self.move_in_event, True, 1))
                return
            self.move_in_event(i, j)

    def move_out_event(self):
        """
        Retrieve grid square, call move out on grid square, schedule move-in event for random time in the future
        """
        from main import Event
        from grid import GridSquare
        sq: GridSquare = self.gl.grid.get_grid_square(self.home_location[0], self.home_location[1])
        loc = self.home_location
        self.home_location = (-1, -1)
        sq.moveout(self)
        # Create new move in event to add to the future event list
        # TODO: Looks like the event is not being scheduled according to probability distribution. Needs to be fixed
        event = Event(self.gl.clock + random.randint(0, 3), self.pid, self.move_in_event, True, 1)
        # print("moved out of " + str(loc[0]) + ' ' + str(loc[1]))
        self.schedule_event(event)

    def move_in_event(self, row, col):
        """
        Move into grid square, sample probability distribution for appropriate move out time. Schedule move out event
        according to the current global simulation time plus randomly sampled variable.
        :param row:
        :param col:
        """
        from main import Event
        from grid import GridSquare
        self.home_location = (row, col)
        loc = self.home_location
        sq: GridSquare = self.gl.grid.get_grid_square(self.home_location[0], self.home_location[1])
        sq.movein(self)
        years = 0
        years = self.sample_move_out_distribution(years)
        t = self.gl.clock + years
        event = Event(t, self.pid, self.move_out_event, True, 0)
        # print("moved into " + str(loc[0]) + ' ' + str(loc[1]))
        self.schedule_event(event)

    def schedule_event(self, event_i: Event):
        """
        Copy of the schedule event method in main.py. Accesses the future event list through the global variables
        stored in the Person object
        :param event_i:
        """
        from main import heappush
        self.next_event = event_i
        heappush(self.gl.fel, event_i)

    """ STATIC METHODS: THE FOLLOWING ARE USED TO SAMPLE FROM PROBABILITY DISTRIBUTIONS DEFINED IN THE CSV FILES"""
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

    @staticmethod
    def sample_move_out_distribution(years):
        from main import move_out_data
        rn = random.randint(0, 100) / 100
        for i in range(len(move_out_data) - 1, -1, -1):
            if move_out_data[i] < rn:
                years = i + 1
                break
        return years
