#!/usr/bin/python3

# move the blank, not the surrounding pieces, this makes the 

import sys

from utils import print_header
from puzzle_agent import PuzzleAgent, PuzzleAction, PuzzleState, h1_hueristic, h2_hueristic

def run(filename: str):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    print_header()

    agent = PuzzleAgent()
    
    for (i, line) in enumerate(lines):
        sp = line.replace('\n', '').split(' ')
        cmd = sp[0]
        print("=" * 50)
        print(line)

        if cmd == "setState":
            # create the state from the 3 strings provided
            state_str = sp[1] + sp[2] + sp[3]
            # replace "b" with "0" to fit our needs
            state = PuzzleState.from_str(state_str)

            # send new state to the agent
            agent.set_state(state)
        elif cmd == "printState":
            # print the agents state
            agent.print_state()
        elif cmd == "move":
            # get the direction string from position 2
            direction_str = sp[1]
            # convert the string into an enum element
            action: PuzzleAction = None
            if direction_str == "left":
                action = PuzzleAction.Left
            elif direction_str == "Right":
                action = PuzzleAction.Right
            elif direction_str == "Up":
                action = PuzzleAction.Up
            elif direction_str == "Down":
                action = PuzzleAction.Down
            else:
                print("Direction str error")
                exit(1)

            # send the action to the agent
            agent.move(action)
        elif cmd == "randomizeState":
            # get n from arguments
            n = int(sp[1])
            # send n to agent for randomization
            agent.randomize_state(n)
        elif cmd == "solve":
            # get the desired search method
            method = sp[1]

            if method == "A-star":
                hueristic_str = sp[2]
                h = None
                if hueristic_str == "h1":
                    h = h1_hueristic
                elif hueristic_str == "h2":
                    h = h2_hueristic
                else:
                    print("Invalid hueristic ({})".format(hueristic_str))
                    exit(1)

                result = agent.a_star(h)
                print(str(result))
            elif method == "beam":
                result = agent.beam_search(int(sp[2]), h1_hueristic)
                print(str(result))
            else:
                print("Invalid solve method ({}) on line {}.".format(method, i))
                exit(1)
        elif cmd == "maxNodes":
            n = int(sp[1])
            agent.set_max_nodes(n)
        else:
            print("Invalid command on line {}".format(i))
            exit(1)

    print("=" * 50)
    print("Finished running program!")


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) < 1:
        exit(1)
    # cmd_file = sys.argv[1]
    cmd_file = "test.txt"
    run(cmd_file)
    # test()
