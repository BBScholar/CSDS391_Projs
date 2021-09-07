from typing import *
from typing import Final
from enum import Enum
from abc import abstractmethod

import random


class GenericAction(Enum):
    @classmethod
    def list(cls):
        return list(cls)


class GenericState:

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass

State = TypeVar("State", bound=GenericState)
Action = TypeVar("Action", bound=GenericAction)


class GenericAgent(Generic[State, Action]):

    rng_seed: Final[int] = 69 + 420

    def __init__(self):
        self.state = None
        self.max_nodes = 0
        self.rng = random.Random(self.rng_seed)

    @staticmethod
    @abstractmethod
    def get_actions() -> List[Action]:
        pass

    @staticmethod
    @abstractmethod
    def calculate_state(state: State, action: Action) -> Optional[State]:
        pass

    @classmethod
    def expand_state(cls, state: State) -> List[Tuple[Action, State]]:
        states: List[Tuple[Action, State]] = []
        for action in cls.get_actions():
            new_state = cls.calculate_state(state, action)
            if new_state is not None:
                states.append((action, new_state))
        return states

    def move(self, action: Action):
        new_state = self.calculate_state(self.state, action)
        if new_state is not None:
            self.state = new_state

    def randomize_state(self, n: int):
        for _ in range(n):
            while True:
                action = self.rng.choice(self.get_actions())
                new_state = self.calculate_state(self.state, action)
                if new_state is not None:
                    self.state = new_state
                    break
                else:
                    continue

    def set_state(self, state: State):
        self.state = state

    def set_max_nodes(self, n: int):
        self.max_nodes = n

    def print_state(self):
        print(str(self.state))


