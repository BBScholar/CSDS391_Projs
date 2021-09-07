from typing import *

from generic_agent import GenericAgent, GenericState, GenericAction
from algos import a_star, SearchAlgoReturn


class PuzzleState(GenericState):

    def __init__(self, state: List[int], blank_idx: int):
        assert len(state) == 9
        assert blank_idx >= 0 and blank_idx < 9

        self.data = state
        self.blank_idx = blank_idx

    def __str__(self) -> str:
        s: str = ""
        for i, v in enumerate(self.data):
            if i % 3 == 0 and i != 0:
                s += "\n"
            s += str(v) + " "
        return s

    def __eq__(self, other) -> bool:
        if not isinstance(other, PuzzleState):
            return False
        for a, b in zip(self.data, other.data):
            if a != b:
                return False
        return True

    def __hash__(self) -> int:
        return hash(tuple(self.data))

    @staticmethod
    def from_str(s: str) -> 'PuzzleState':
        assert len(s) == 9
        s.replace("b", "0")
        idx = s.find("0")
        l = list(map(int, list(s)))
        return PuzzleState(l, idx)


class PuzzleAction(GenericAction):
    Up = 1
    Down = 2
    Left = 3
    Right = 4


class PuzzleAgent(GenericAgent[PuzzleState, PuzzleAction]):

    goal_state: Final[PuzzleState] = PuzzleState.from_str("012345678")

    def __init__(self):
        super().__init__()
        self.state = self.goal_state

    @staticmethod
    def get_actions() -> List[PuzzleAction]:
        return list(PuzzleAction)

    @staticmethod
    def calculate_state(state: PuzzleState, action: PuzzleAction) -> Optional[PuzzleState]:
        idx = state.blank_idx

        on_top = (idx == 0) or (idx == 1) or (idx == 2)
        on_bottom = (idx == 6) or (idx == 7) or (idx == 8)
        on_left = (idx == 0) or (idx == 3) or (idx == 6)
        on_right = (idx == 2) or (idx == 5) or (idx == 8)

        d_idx: int = 0

        if action == PuzzleAction.Up:
            if on_top:
                return None
            d_idx = -3
        elif action == PuzzleAction.Down:
            if on_bottom:
                return  None
            d_idx = 3
        elif action == PuzzleAction.Left:
            if on_left:
                return None
            d_idx = -1
        elif action == PuzzleAction.Right:
            if on_right:
                return None
            d_idx = 1
        else:
            print("This should never happen")
            exit(1)

        new_idx: int = idx + d_idx

        new_state = state.data.copy()
        new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
        return PuzzleState(new_state, new_idx)

    def a_star(self, hueristic: Callable[[PuzzleState, PuzzleState], int]) -> SearchAlgoReturn:
        return a_star(self, self.goal_state, hueristic)



def h1_hueristic(goal_state: PuzzleState, state: PuzzleState) -> int:
    sum = 0

    # TODO: does this need to be divided by 2?
    for g, s in zip(goal_state.data, state.data):
        if not g == s:
            sum += 1
    return sum

# O(1) complexity for fixed size
# O(n^2) for NxN puzzles
# TODO: can this be optimized? I dont think I can do better than n^2 since
# there isnt any ordering. Maybe somthing with a hashtable? Doesnt matter for now
def h2_hueristic(goal_state: PuzzleState, state: PuzzleState) -> int:
    sum = 0

    # loop through every element in the goal state
    for i in range(0, 9):
        # goal value at idx i
        g = goal_state.data[i]
        # x coord of g
        g_x = i % 3
        # y coord of g
        g_y = int(i / 3)

        # loo
        for j in range(0, 9):
            s = state.data[j]
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
                sum += abs(g_x - s_x) + abs(g_y - s_y)
            else:
                continue

    return sum
