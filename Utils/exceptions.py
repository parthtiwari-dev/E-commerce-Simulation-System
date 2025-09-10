"""
Custom Exceptions Module

Purpose:
    Defines all project-specific exception classes for the e-commerce simulation system.
    Enables clear, centralized, and reusable error reporting across services and models.

Key Responsibilities:
    - Define custom exceptions for common error scenarios: OutOfStock, PaymentFailure, InvalidCoupon, etc.
    - Make business failures explicit and safely catchable by workflows and tests.
    - Facilitate DRY error handling and debugging by importing from a single source.

Example Classes:
    OutOfStockError:      Raised when requested stock is unavailable.
    PaymentFailedError:   Raised when a simulated payment attempt fails.
    InvalidCouponError:   Raised when a coupon is not valid for a cart or order.
    TransactionError:     Raised for failures in multi-step transaction blocks.

Notes:
    Update this module as your system adds new error cases.
"""
