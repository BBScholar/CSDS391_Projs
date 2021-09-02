#!/usr/bin/python3

# move the blank, not the surrounding pieces, this makes the 

import sys
import math
import random
from enum import Enum, unique

def run(filename: str):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    state = State()
    
    for (i, line) in enumerate(lines):
        sp = line.split(' ')
        cmd = sp[0]

        if cmd == "setState":
            state_str = sp[1] + sp[2] + sp[3]
            state.set_state(state_str)
        elif cmd == "printState":
            print(state)
        elif cmd == "move":
            direction_str = sp[1]
            direction = Direction[direction_str]
            state.move(direction)
        elif cmd == "randomizeState":
            n = int(sp[1])
            state.randomize_state(n)
        elif cmd == "solve":
            method = sp[1]
            if method == "A-star":
                state.a_star(sp[2])
            elif method == "beam":
                state.beam(int(sp[2]))
            else:
                print("Invalid solve method ({}) on line {}.".format(method, i))
                exit(1)
        elif cmd == "maxNodes":
            n = int(sp[1])
            state.set_max_nodes(n)
        else:
            print("Invalid command on line {}".format(i))
            exit(1)


def test():
    state = State()

    state.set_state("b12345678")     
    state.randomize_state(5)
        

if __name__ == "__main__":
    print(sys.argv)
    n = len(sys.argv)
    if n < 1:
        exit(1)
    # cmd_file = sys.argv[1]
    cmd_file = "test.txt"
    # run(cmd_file)
    test()