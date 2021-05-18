from typing import List, Optional, TypeVar, Tuple, Dict, Generic

from time import time

import heapq

T = TypeVar('T')


class LRUTuple(tuple):
    def __init__(self, key: Tuple[str]) -> None:
        self.key = key
        self.time = time()

    def __lt__(self, other) -> bool:
        return self.time < other.time

    def __gt__(self, other) -> bool:
        return not self.time < other.time

class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._data: List[T] = []

    @property
    def is_empty(self) -> bool:
        return not self._data

    def add(self, v: T) -> None:
        heapq.heappush(self._data, v)

    def pop_queue(self) -> Optional[T]:
        if not self.is_empty:
            return heapq.heappop(self._data)
        else:
            return None

    def _heapify(self) -> None:
        heapq.heapify(self._data)

    def peek(self) -> Optional[T]:
        if not self.is_empty:
            return self._data[0]
        else:
            return None

    def __repr__(self) -> str:
        return repr(self._data)


class LRUCache:
    def __init__(self, limit: int) -> None:
        self._data: Dict[str, T] = {}
        self.limit = limit
        self._keyqueue: PriorityQueue[LRUTuple] = PriorityQueue()

    def _update_key_time(self, key: str) -> None:
        self._keyqueue._data[self._keyqueue._data.index((key,))].time = time()
        self._keyqueue._heapify()

    def put(self, key: str, value: T) -> None:
        if len(self._keyqueue._data) < self.limit:
            if key not in self._data:
                self._data[key] = value
                self._keyqueue.add(LRUTuple((key,)))
            else:
                self._data[key] = value
                self._update_key_time(key)
        else:
            # remove lru key
            poped_key = self._keyqueue.pop_queue()
            self._data.pop(poped_key[0])
            self.put(key, value)

    def get(self, key: str) -> Optional[T]:
        if key in self._data:
            self._update_key_time(key)
            return self._data[key]
        else:
            return None

    def __repr__(self) -> str:
        return repr([(k[0], k.time) for k in self._keyqueue._data])

