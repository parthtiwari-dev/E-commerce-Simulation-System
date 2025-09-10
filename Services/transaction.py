"""
Transaction and Atomic Operation Utilities Module

Purpose:
    Provides context managers and helpers for atomic, all-or-nothing operations
    across inventory, payment, and order creation. Ensures system consistency
    by rolling back partial state changes on failure (inventory, payments, orders).

Key Responsibilities:
    - Handle atomic checkout workflows (reserve stock, process payment, finalize order)
      so that if any step fails, previous steps are safely rolled back.
    - Support "with" statement context for transactional blocks.
    - Integrate with logging and exception services for robust error handling.
    - Enable simulation of real-world transactional safety for bulk/stress testing.

Example Classes/Methods:
    TransactionContext: Context manager for atomic order placement.
    begin(): Manual transaction start.
    commit(): Commit all pending changes.
    rollback(): Revert all changes if a workflow step fails.
    run_atomic(func, *args, **kwargs): Run a function atomically with rollback-on-failure.

Notes:
    Critical for scaling reliability—especially with concurrent checkouts,
    high traffic, or in a multi-threaded/bulk order simulation environment.
"""
"""
Transaction and Atomic Operation Utilities Module
(Put the earlier docstring here!)
"""

from typing import Callable, Any

class TransactionContext:
    """
    Simple context manager to simulate atomic operations for cart/order/stock/payment.
    On failure, can trigger manual rollback logic.
    """
    def __init__(self, rollback_funcs=None):
        # rollback_funcs is a list of callables (usually lambdas) to call on rollback
        self.rollback_funcs = rollback_funcs if rollback_funcs is not None else []

    def add_rollback(self, func: Callable[[], None]):
        self.rollback_funcs.append(func)

    def __enter__(self):
        # Start transaction (could lock resources, log start)
        print("[TRANSACTION] Begin")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"[TRANSACTION] Error occurred: {exc_val}, rolling back.")
            for func in reversed(self.rollback_funcs):
                func()
            print("[TRANSACTION] Rollback complete.")
        else:
            print("[TRANSACTION] Commit.")

