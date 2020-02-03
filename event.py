class Event:

    def __init__(self, t: float, pid: int, fun: classmethod, is_thread: bool,
                 type: int):
        self.time_stamp = t
        self.process_id = pid
        self.function = fun
        self.is_thread = is_thread
        self.type = type

    def __gt__(self, other):
        return self.time_stamp > other.time_stamp

    def __lt__(self, other):
        return self.time_stamp < other.time_stamp

    def __eq__(self, other):
        return self.time_stamp == other.time_stamp

    def __ne__(self, other):
        return not self.__eq__(other)
