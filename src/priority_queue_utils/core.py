"""A binary min-heap with stable handles and decrease-key support.

The heap stores ``(key, priority)`` pairs.  Each key is associated with a
unique integer handle returned by :meth:`push`.  The handle can be used to
change the priority of an entry in O(log n) time without rebuilding the heap.

Only one entry per key is allowed; pushing a duplicate key raises
:class:`ValueError`.

Priorities are compared with ``<``.  They may be any objects that support
rich comparison, but mixed types that cannot be compared will raise
``TypeError`` at the point of comparison.
"""

from __future__ import annotations

from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar

K = TypeVar("K")
P = TypeVar("P")


class IndexedMinHeap(Generic[K, P]):
    """A binary min-heap with indexed decrease-key support.

    Internally the heap is a list of ``[key, priority, handle]`` entries.
    A dictionary maps each key to the index of its entry in the list, so
    that the entry can be located in O(1) time and then sifted up or down
    in O(log n) time.

    Handles are monotonically increasing integers.  They are never reused,
    even after removal, so a stale handle can be detected by comparing it
    with the handle stored at the entry's index.
    """

    __slots__ = ("_heap", "_index", "_next_handle")

    def __init__(self) -> None:
        self._heap: List[List[Any]] = []
        self._index: Dict[K, int] = {}
        self._next_handle: int = 0

    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return bool(self._heap)

    def __contains__(self, key: object) -> bool:
        return key in self._index

    def push(self, key: K, priority: P) -> int:
        """Insert *key* with *priority* and return its handle.

        Raises :class:`ValueError` if *key* is already present.
        """
        if key in self._index:
            raise ValueError(f"key already present: {key!r}")
        handle = self._next_handle
        self._next_handle += 1
        entry = [key, priority, handle]
        self._heap.append(entry)
        self._index[key] = len(self._heap) - 1
        self._sift_up(len(self._heap) - 1)
        return handle

    def peek(self) -> Tuple[K, P]:
        """Return the ``(key, priority)`` pair with the smallest priority.

        Raises :class:`IndexError` if the heap is empty.
        """
        if not self._heap:
            raise IndexError("peek from an empty heap")
        key, priority, _ = self._heap[0]
        return key, priority

    def pop(self) -> Tuple[K, P]:
        """Remove and return the ``(key, priority)`` pair with the smallest priority.

        Raises :class:`IndexError` if the heap is empty.
        """
        if not self._heap:
            raise IndexError("pop from an empty heap")
        key, priority, _ = self._heap[0]
        self._remove_at(0)
        return key, priority

    def decrease_key(self, key: K, new_priority: P) -> None:
        """Lower the priority of *key* to *new_priority*.

        If *new_priority* is not strictly smaller than the current priority,
        the heap is left unchanged.  This makes the operation safe to call
        blindly (for example, when relaxing an edge) without checking the
        current value first.

        Raises :class:`KeyError` if *key* is not present.
        """
        try:
            index = self._index[key]
        except KeyError:
            raise KeyError(key) from None
        entry = self._heap[index]
        if new_priority < entry[1]:
            entry[1] = new_priority
            self._sift_up(index)

    def priority(self, key: K) -> P:
        """Return the current priority of *key*.

        Raises :class:`KeyError` if *key* is not present.
        """
        try:
            index = self._index[key]
        except KeyError:
            raise KeyError(key) from None
        return self._heap[index][1]

    def remove(self, key: K) -> Tuple[K, P]:
        """Remove *key* from the heap and return its ``(key, priority)`` pair.

        Raises :class:`KeyError` if *key* is not present.
        """
        try:
            index = self._index[key]
        except KeyError:
            raise KeyError(key) from None
        entry = self._heap[index]
        self._remove_at(index)
        return entry[0], entry[1]

    def _remove_at(self, index: int) -> None:
        """Remove the entry at *index* and restore the heap property."""
        last = self._heap.pop()
        del self._index[last[0]]
        if index < len(self._heap):
            self._heap[index] = last
            self._index[last[0]] = index
            self._sift_down(index)
            self._sift_up(index)

    def _sift_up(self, index: int) -> None:
        """Move the entry at *index* toward the root until the heap property holds."""
        heap = self._heap
        entry = heap[index]
        priority = entry[1]
        while index > 0:
            parent = (index - 1) >> 1
            parent_entry = heap[parent]
            if priority < parent_entry[1]:
                heap[index] = parent_entry
                self._index[parent_entry[0]] = index
                index = parent
            else:
                break
        heap[index] = entry
        self._index[entry[0]] = index

    def _sift_down(self, index: int) -> None:
        """Move the entry at *index* toward the leaves until the heap property holds."""
        heap = self._heap
        size = len(heap)
        entry = heap[index]
        priority = entry[1]
        while True:
            left = (index << 1) + 1
            if left >= size:
                break
            right = left + 1
            child = left
            if right < size and heap[right][1] < heap[left][1]:
                child = right
            child_entry = heap[child]
            if child_entry[1] < priority:
                heap[index] = child_entry
                self._index[child_entry[0]] = index
                index = child
            else:
                break
        heap[index] = entry
        self._index[entry[0]] = index
