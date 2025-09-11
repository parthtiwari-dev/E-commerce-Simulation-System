"""
Cache Utilities Module

Purpose:
    Implements temporary data caching (e.g. LRU, LFU, basic dict) for the e-commerce system.
    Can be used for frequently accessed data such as popular products or price lookup acceleration.

Key Responsibilities:
    - Provide reusable cache classes or decorators for any module needing in-memory memoization.
    - Support capacity limits and automatic eviction strategies (for LRU, etc.).
    - Demonstrate knowledge of production-performance best practices.

Example Classes:
    LRUCache:   Least-recently-used cache implementation.
    SimpleCache: Basic in-memory dictionary cache.

Notes:
    Caching is optional but a great coding interview “bonus” and can reduce repeated computations.
"""

from collections import OrderedDict


class SimpleCache:
    def __init__(self):
        self.store = {}

    def set(self, key, value):
        self.store[key] = value

    def get(self, key):
        return self.store.get(key, None)

    def clear(self):
        self.store.clear()


class LRUCache:
    def __init__(self, capacity: int = 5):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return None
        # Move accessed key to the end (mark as most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]

    def set(self, key, value):
        if key in self.cache:
            # Update and move to end
            self.cache.move_to_end(key)
        self.cache[key] = value
        # Evict least recently used
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def __repr__(self):
        return str(self.cache)
