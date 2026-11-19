import unittest

from priority_queue_utils import IndexedMinHeap


class TestIndexedMinHeap(unittest.TestCase):
    def test_push_and_pop_order(self):
        heap = IndexedMinHeap()
        heap.push("a", 3)
        heap.push("b", 1)
        heap.push("c", 2)
        self.assertEqual(heap.pop(), ("b", 1))
        self.assertEqual(heap.pop(), ("c", 2))
        self.assertEqual(heap.pop(), ("a", 3))

    def test_peek_does_not_remove(self):
        heap = IndexedMinHeap()
        heap.push("x", 10)
        self.assertEqual(heap.peek(), ("x", 10))
        self.assertEqual(len(heap), 1)

    def test_peek_empty_raises(self):
        heap = IndexedMinHeap()
        with self.assertRaises(IndexError):
            heap.peek()

    def test_pop_empty_raises(self):
        heap = IndexedMinHeap()
        with self.assertRaises(IndexError):
            heap.pop()

    def test_duplicate_key_raises(self):
        heap = IndexedMinHeap()
        heap.push("k", 1)
        with self.assertRaises(ValueError):
            heap.push("k", 2)

    def test_decrease_key_moves_to_front(self):
        heap = IndexedMinHeap()
        heap.push("a", 5)
        heap.push("b", 6)
        heap.push("c", 7)
        heap.decrease_key("c", 1)
        self.assertEqual(heap.peek(), ("c", 1))
        self.assertEqual(heap.pop(), ("c", 1))
        self.assertEqual(heap.pop(), ("a", 5))
        self.assertEqual(heap.pop(), ("b", 6))

    def test_decrease_key_missing_raises(self):
        heap = IndexedMinHeap()
        with self.assertRaises(KeyError):
            heap.decrease_key("nope", 1)

    def test_decrease_key_noop_for_larger_priority(self):
        heap = IndexedMinHeap()
        heap.push("a", 1)
        heap.push("b", 2)
        heap.decrease_key("b", 5)
        self.assertEqual(heap.peek(), ("a", 1))
        self.assertEqual(heap.priority("b"), 2)

    def test_priority_lookup(self):
        heap = IndexedMinHeap()
        heap.push("a", 42)
        self.assertEqual(heap.priority("a"), 42)

    def test_priority_missing_raises(self):
        heap = IndexedMinHeap()
        with self.assertRaises(KeyError):
            heap.priority("missing")

    def test_remove_returns_entry(self):
        heap = IndexedMinHeap()
        heap.push("a", 1)
        heap.push("b", 2)
        heap.push("c", 3)
        self.assertEqual(heap.remove("b"), ("b", 2))
        self.assertEqual(len(heap), 2)
        self.assertEqual(heap.pop(), ("a", 1))
        self.assertEqual(heap.pop(), ("c", 3))

    def test_remove_missing_raises(self):
        heap = IndexedMinHeap()
        with self.assertRaises(KeyError):
            heap.remove("missing")

    def test_contains(self):
        heap = IndexedMinHeap()
        heap.push("a", 1)
        self.assertIn("a", heap)
        self.assertNotIn("b", heap)

    def test_bool_and_len(self):
        heap = IndexedMinHeap()
        self.assertFalse(heap)
        self.assertEqual(len(heap), 0)
        heap.push("a", 1)
        self.assertTrue(heap)
        self.assertEqual(len(heap), 1)

    def test_handles_are_unique_and_monotonic(self):
        heap = IndexedMinHeap()
        h1 = heap.push("a", 1)
        h2 = heap.push("b", 2)
        self.assertNotEqual(h1, h2)
        self.assertLess(h1, h2)

    def test_large_random_sequence(self):
        import random

        rng = random.Random(1234)
        heap = IndexedMinHeap()
        keys = list(range(200))
        rng.shuffle(keys)
        for k in keys:
            heap.push(k, k)
        popped = [heap.pop()[0] for _ in range(len(heap))]
        self.assertEqual(popped, sorted(keys))


if __name__ == "__main__":
    unittest.main()
