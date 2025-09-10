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
