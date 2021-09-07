
from dataclasses import dataclass, field
from typing import Generic, Type, TypeVar, Tuple, List, Optional
import heapq

T = TypeVar('T')

# min priority queue
class PriorityQueue(Generic[T]):

    def __init__(self):
        self.data = []
       
    def push(self, value: T):
        heapq.heappush(self.data, value)

    def peak(self) -> Optional[T]:
        if self.is_empty():
            return None
        return self.data[0]

    def pop(self) -> Optional[T]:
        if self.is_empty():
            return None
        return heapq.heappop(self.data)

    def is_empty(self) -> bool:
        return len(self.data) == 0
    
    def has_value(self) -> bool:
        return not self.is_empty()

    def __len__(self) -> int:
        return len(self.data)
