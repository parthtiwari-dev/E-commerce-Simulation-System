"""
Random Data Generator for Stress Testing

Purpose:
    Provides helper functions to generate synthetic users, products, and carts for high-volume testing
    of the e-commerce system. Enables simulation of realistic, large-scale e-commerce scenarios.

Key Responsibilities:
    - Generate a configurable number of sample users, products, and orders with randomized attributes.
    - Support batch creation to populate the system prior to stress test runs.
    - Optionally, support seeding for reproducible tests.

Example Methods:
    generate_products(n):        Returns a list of n Product objects with random details.
    generate_users(n):           Returns a list of n User objects.
    generate_carts(users, ...):  Returns carts filled by users with randomized selections.

Notes:
    Used only for bulk/system stress testing—never in production logic.
"""
