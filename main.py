""" Import statements """
from queue import PriorityQueue
from threading import Condition

def main():
    # Priority queue of time stamped threads
    fel = PriorityQueue()
    wait_list = []

    waiting_condition = Condition()

    while (True):
        print(1)



if __name__ == "__main__":
    main()