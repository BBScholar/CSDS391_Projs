from dataclasses import dataclass, field
from enum import Enum, unique, auto
from typing import Tuple, List, Callable, Any
import random, math

from lib.priority_queue import PriorityQueue


@unique
class Actions(Enum):
    Up = (1, "up")
    Down = (2, "down")
    Left = (3, "left")
    Right = (4, "right")

# A class representing a state of the puzzle
# formatted as a character array with the followign indicies
# 0 1 2
# 3 4 5
# 6 7 8
# 0 represents the blank space, 1-8 represent the numbered tiles
class State:

    def __init__(self, state: List[int], blank_idx:int = None):
        self.state = state

        if blank_idx == None:
            # find blank idx if it isnt provided
            for i, c in enumerate(state):
                if c == 0:
                    self.blank_idx = i
                    break
        else:
            self.blank_idx = blank_idx

    def is_valid(self) -> bool:
        contains = [False] * 9
        for c in self.state:
            contains[c] ^= True
        
        res = True
        for c in contains:
            res = res and c
        return res

@dataclass (order=True)
class SearchNode:
    # moves represents the number of tile moved to arrive at the current state
    depth: int = field(compare=False)
    # cost represents the total cost of the node (moves + hueristic(state))
    cost: int = field(compare=True)
    #current state
    state: State = field(comapre=False)
    # action enacted on parent in order to arrive at the current state
    action: Actions = field(compare=False, default=None)
    # previous state, used so we can backtrack after finding the solution
    parent: Any = field(compare=False, default=None)


# takes the current state and the desired action and returns the 
# resulting state. Returns None if input is invalid
def calculate_state(action: Actions, state: State) -> State:
    blank_idx = state.blank_idx

    # calculate the bounds
    is_on_left = blank_idx == 0 or blank_idx == 3 or blank_idx == 6
    is_on_right = blank_idx == 2 or blank_idx == 5 or blank_idx == 8
    is_on_top = blank_idx == 0 or blank_idx == 1 or blank_idx == 2
    is_on_bottom = blank_idx == 6 or blank_idx == 7 or blank_idx == 8

    d_idx: int = None
    
    #check if move will be valid and determine next state
    if action is Actions.Left:
        if is_on_left:
            return None
        d_idx = -1
    elif action is Actions.Right:
        if is_on_right:
            return None
        d_idx = 1
    elif action is Actions.Up:
        if is_on_top:
            return None
        d_idx = -3
    elif action is Actions.Down:
        if is_on_bottom:
            return None
        d_idx = 3

    # calculate the desired position of the blank
    new_blank_idx = blank_idx + d_idx

    # copy the state array from the previous state
    new_state = state.state.copy()
    
    # swap the positions (without a temp variable)
    new_state[new_blank_idx], new_state[blank_idx] = new_state[blank_idx], new_state[new_blank_idx]

    # returns state
    return State(new_state, new_blank_idx)

def expand(state: State) -> List[State]:
    new_states = []
    for action in Actions:
        new_state = calculate_state(action, state)
        if new_state == None:
            pass
        else:
            new_states.append(new_state)
    return new_states

class PuzzleAgent:
    # sorry this is very hacky
    goal_state = State(list(map(int,list("012345678"))), 0)

    def __init__(self):
        # initial state
        self.state = PuzzleAgent.goal_state
        # assign rng to we can test with same seed
        self.random = random.Random(69)
        # 
        self.max_nodes = 0

    def set_max_nodes(self, n: int):
        self.max_nodes = n

    def set_state(self, state: State):
        self.state = state

    def move(self, action: Actions):
        new_state = calculate_state(action, self.state)
        if new_state == None:
            return
        self.state = new_state

    def randomize_state(self, n: int):
        # generate n random moves
        for _ in range(n):
            # generate actions until we recieve a valid move
            while True:
                action = self.random.choice(list(Actions))
                next_state = calculate_state(action, self.state)
                if next_state == None:
                    continue
                else:
                    break
                          
    def beam_search(self, k: int) -> Tuple[int, List[Actions]]:
        pass

    def collect_actions(self, final_node: SearchNode) -> List[Actions]:
        actions = []
        # iterate over the 
        current_node = final_node
        while current_node != None:
            actions.append(current_node.action)
            current_node = current_node.parent
        actions.reverse()
        return actions

    def a_star(self, hueristic: Callable[[State], int]) -> Tuple[int, List[Actions]]:
        
        # define frontier variable
        frontier = PriorityQueue(None)
        # push the initial state, has a cost of 0 moves + whatever the hueristic score is
        initial_node = SearchNode(moves = 0, cost=hueristic(self.state))
        frontier.push(initial_node)
        
        # loop until we find the goal or run out of nodes to visit
        while not frontier.is_empty():
            current_cost, current_state = frontier.pop()

            if current_state == PuzzleAgent.goal_state:
                actions = self.collect_actions(current_state)
                return (current_cost, [])

            next_states = expand(current_state)
            for state in next_states:
                weight = current_cost + 1
                frontier.push()

            # calculate scores



    def print_state(self):
        # TODO: check this
        for i in range(3):
            for j in range(3):
                print(self.state.state[3 * i + j] +  " ", end="")
            print("")


# O(1) complexity with a fixed size
# O(n) for NxN puzzles
def h1_hueristic(goal_state: State, state: State) -> int:
    sum = 0

    # TODO: does this need to be divided by 2?
    for g, s in zip(goal_state.state, state.state):
        if not g == s:
            sum += 1
    return sum

# O(1) complexity for fixed size
# O(n^2) for NxN puzzles
# TODO: can this be optimized? I dont think I can do better than n^2 since
# there isnt any ordering. Maybe somthing with a hashtable? Doesnt matter for now
def h2_hueristic(goal_state: State, state: State) -> int:
    sum = 0

    # loop through every element in the goal state
    for i in range(0, 9):
        # goal value at idx i
        g = goal_state.state[i]
        # x coord of g
        g_x = i % 3
        # y coord of g
        g_y = int(i / 3)

        # loo
        for j in range(0, 9):
            s = state.state[j]
            # check if s and g are equal
            # if they are calculate the distance between the two
            if s == g:
                # if the indicies are the same, s is in the correct position
                # so save some cpu cycles and memory by breaking early
                if i == j:
                    sum += 0
                    break
                # calculate coordinates of s
                s_x = j % 3
                s_y = int(j / 3)
                # calculate cost
                sum += math.abs(g_x - s_x) + math.abs(g_y - s_y)
            else:
                continue

    return sum