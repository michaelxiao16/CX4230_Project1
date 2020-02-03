from threading import Condition


class Event:

    def __init__(self, t: float, pid: int, fun: classmethod, is_thread: bool,
                 cv: Condition):
        self.time_stamp = t
        self.process_id = pid
        self.function = fun
        self.is_thread = is_thread
        self.cv = cv

    def __gt__(self, other):
        return self.time_stamp > other.timestamp

    def __lt__(self, other):
        return self.time_stamp < other.timestamp

    def __eq__(self, other):
        return self.time_stamp == other.timestamp

    def __ne__(self, other):
        return not self.__eq__(other)