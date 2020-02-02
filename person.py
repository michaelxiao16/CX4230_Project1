from threading import Thread, Condition
from main import Event, clock


class Person(Thread):
    """ A class to represent people in simulation """

    def get_income(self):
        return self.income

    def get_price_point(self):
        return self.price_point

    def __init__(self, income: float, price_point: float,
                 cv_time: Condition, cv_housing: Condition,
                 next_event: Event, pid: int):
        super().__init__()
        self.income = income
        self.price_point = price_point
        self.cv_time = cv_time
        self.cv_housing = cv_housing
        self.next_event = next_event
        self.pid = pid

    def run(self):
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
            while grid.find_appropriate_housing() == None:
                cv.wait()
            event.function()
            self.next_event = None
            cv.release()

    def move_out_event(self):
        pass

    def move_in_event(self):
        pass
