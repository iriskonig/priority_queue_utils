# priority_queue_utils

A binary min-heap with stable handles and O(log n) decrease-key, so you can
relax an edge or lower a cost without rebuilding the queue.

## Usage

```python
from priority_queue_utils import IndexedMinHeap

heap = IndexedMinHeap()
heap.push("a", 5)
heap.push("b", 2)
heap.push("c", 9)

heap.decrease_key("c", 1)
assert heap.peek() == ("c", 1)
assert heap.pop() == ("c", 1)
assert heap.pop() == ("b", 2)
assert heap.pop() == ("a", 5)
```

## Why this exists

A plain `heapq` gives you a heap but not a way to find an entry again after
you have pushed it.  Dijkstra-style algorithms need to lower the priority of
a node that is already in the queue.  The usual workaround is to push a new
entry and skip stale ones when they pop, which grows the heap and makes the
worst case worse.  `IndexedMinHeap` keeps a dictionary from key to heap
position, so `decrease_key` is a real sift-up in O(log n).

The trade-off is that keys must be hashable and unique.  Pushing a duplicate
key raises `ValueError` rather than silently replacing the old entry.

## Edge cases

`decrease_key` only lowers a priority.  If you pass a larger priority it is a
no-op, which makes it safe to call blindly while relaxing an edge.  Removing
the last element, popping the only element, and calling `peek` or `pop` on an
empty heap are all handled explicitly: `peek` and `pop` raise `IndexError`,
and `remove` and `decrease_key` raise `KeyError` for a missing key.

## API

- `IndexedMinHeap()` — construct an empty heap.
- `push(key, priority) -> int` — insert and return a unique handle.
- `peek() -> (key, priority)` — smallest priority without removing.
- `pop() -> (key, priority)` — remove and return the smallest priority.
- `decrease_key(key, new_priority) -> None` — lower a priority in place.
- `priority(key) -> priority` — current priority for a key.
- `remove(key) -> (key, priority)` — remove an arbitrary key.
- `key in heap`, `len(heap)`, `bool(heap)` — membership and size.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

