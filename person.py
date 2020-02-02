from threading import Thread
class Person(Thread):
    """ A class to represent people in simulation """


    def get_time(self):
        return self.time_remaining

    def get_income(self):
        return self.income

    def get_price_point(self):
        return self.price_point

    def __init__(self, time_remaining, income, price_point):
        self.time_remaining = time_remaining
        self.income = income
        self.price_point = price_point

    def run(self):
        """ Called during main loop """
        self.wait()
