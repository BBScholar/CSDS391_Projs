import time
import timeit

import datetime



def print_header():
    print("=" * 50)
    print("Programming Project 1")
    print("Name: Benjamin Scholar")
    print("Class: CSDS 391")
    print("Prof: Dr. Lewicki")
    print("Date: {}".format(str(datetime.date.today())))
    print("=" * 50)


def time(fn):
    start = time.time_ns()
    res = fn()
    elapsed = time.time_ns() - start
    print("Method {} took {} ns".format(fn.__name__, elapsed))
    return res
