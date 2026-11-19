"""Priority queue utilities.

Exports the :class:`IndexedMinHeap` class, which is a binary heap that
supports decrease-key without rebuilding.
"""

from .core import IndexedMinHeap

__all__ = ["IndexedMinHeap"]
