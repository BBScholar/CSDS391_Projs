
from typing import TypeVar, Generic, List, Tuple, Any
from collections import Set

# a light wrapper over the standard library set
# takes an value, gets the hash, and inserts it into the set
class HashSet:

    def __init__(self):
        self.data = set()

    def insert(self, value: Any) -> bool:
        h = hash(value)
        self.data.add(h)

    def contains(self, value: Any) -> bool:
        return hash(value) in self.data

    def remove(value: Any) -> Any:
        h = hash(value)
