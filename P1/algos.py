#!/usr/bin/python3

from typing import *
from dataclasses import dataclass, field
from time import time_ns

from lib.priority_queue import PriorityQueue

from generic_agent import GenericAgent, GenericAction, GenericState


State = TypeVar("State", bound=GenericState)
Action = TypeVar("Action", bound=GenericAction)


Astar_Hueristic = Callable[[State, State], int]
SearchAlgoReturn = Optional[Tuple[int, List[Action]]]


@dataclass(frozen=True)
class SearchResult(Generic[State, Action]):
    success: bool

    nodes_searched: int
    runtime: int

    actions: List[Action] = field(default=None)
    moves: int = field(default=0)

    def __str__(self) -> str:
        s = ""
        if self.success:
            actions = [action.name for action in self.actions]
            s += "Result: Success\n"
            s += f"Moves to goal: {self.moves}\n"
            s += f"Moves: {str(actions)}\n"
        else:
            s += "Result: Failure\n"

        s += f"Nodes searched: {self.nodes_searched}\n"
        s += f"Runtime: {self.runtime} ns"

        return s


@dataclass(order=True)
class SearchNode(Generic[State, Action]):
    state: State = field(compare=False)
    depth: int = field(default=0, compare=False)
    cost: int = field(default=0, compare=True)
    action: Optional[Action] = field(default=None, compare=False)
    parent: Optional['SearchNode[State, Action]'] = field(default=None, compare=False)


def collect_all_actions(final_node: SearchNode[State, Action]) -> List[Action]:
    actions = []
    cursor = final_node
    while cursor.action is not None:
        actions.append(cursor.action)
        cursor = cursor.parent
    actions.reverse()
    return actions

def a_star(agent: GenericAgent[State, Action], goal: State, hueristic: Callable[[State, State], int]) -> SearchResult:
    start_time_ns = time_ns()
    frontier = PriorityQueue[SearchNode]()
    lut: Dict[State, SearchNode] = {}
    nodes_considered: int = 0

    initial_state = agent.state
    initial_node = SearchNode[State, Action](state=initial_state, depth=0, cost=hueristic(initial_state, goal))

    frontier.push(initial_node)
    lut[initial_state] = initial_node

    # TODO: Finish this
    while len(frontier) > 0:
        current_node = frontier.pop()
        current_state = current_node.state
        current_cost = current_node.cost
        current_depth = current_node.depth

        nodes_considered += 1

        if current_state == goal:
            actions = collect_all_actions(current_node)
            return SearchResult(True, nodes_considered, time_ns() - start_time_ns, actions, len(actions))
        elif nodes_considered >= agent.max_nodes:
            print("[ERROR] Max nodes reached, aborting search")
            return SearchResult(False, nodes_considered, time_ns() - start_time_ns)

        for action, state in agent.expand_state(current_state):
            new_depth = current_depth + 1
            new_cost = new_depth + hueristic(state, goal)

            if lut.get(state) is None or new_cost < lut[state].cost:
                # FIXME: this is probably mildly inefficient, we should check to see if the node already exists in memory
                lut[state] = SearchNode(state=state, action=action, parent=current_node, cost=new_cost, depth=new_depth)
                frontier.push(lut[state])

    return SearchResult(False, nodes_considered, time_ns() - start_time_ns)

def beam_search(agent: GenericAgent[State, Action], goal: State, k: int, hueristic: Callable[[State, State], int]) -> SearchResult:
    start_time_ns = time_ns()
    frontier: List[SearchNode] = []
    lut: Dict[State, SearchNode] = {}
    nodes_considered = 0


    initial_state = agent.state
    initial_node = SearchNode[State, Action](state=initial_state, depth=0, cost=hueristic(initial_state, goal))

    frontier.append(initial_node)
    lut[initial_state] = initial_node

    while len(frontier) > 0:
        current_node = frontier.pop(0)
        current_state = current_node.state

        nodes_considered += 1

        if current_node.state == goal:
            actions = collect_all_actions(current_node)
            return SearchResult(True, nodes_considered, time_ns() - start_time_ns, actions, len(actions))
        elif nodes_considered >= agent.max_nodes:
            return SearchResult(False, nodes_considered, time_ns() - start_time_ns)

        for action, state in agent.expand_state(current_state):
            new_depth = current_node.depth + 1
            new_cost = new_depth + hueristic(goal, state) # FIXME

            if lut.get(state) is None or new_cost < lut[state].cost:
                lut[state] = SearchNode(state=state, action=action, parent=current_node, cost=new_cost, depth=new_depth)
                frontier.append(lut[state])

        # trim the statespace by only keeping the k 'best' states in the frontier
        # this operation is kLogk runtime in the worstcase (python uses "Tim sort")
        frontier.sort()
        if len(frontier) > k:
            frontier = frontier[:k]

    return SearchResult(False, nodes_considered, time_ns() - start_time_ns)
