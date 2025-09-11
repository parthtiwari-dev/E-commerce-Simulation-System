"""
Custom Exceptions Module

Purpose:
    Defines all project-specific exception classes for the e-commerce simulation system.
    Enables clear, centralized, and reusable error reporting across services and models.

Key Responsibilities:
    - Define custom exceptions for common error scenarios (e.g., OutOfStock, PaymentFailure, InvalidCoupon).
    - Make business logic failures explicit and safely catchable by workflows and tests.
    - Facilitate DRY error handling and debugging by importing from a single source.

Example Classes:
    OutOfStockError:            Raised when requested stock is unavailable.
    PaymentFailedError:         Raised when a simulated payment attempt fails.
    InvalidCouponError:         Raised when a coupon is invalid, expired, or not applicable.
    DiscountNotApplicableError: Raised when discount conditions are not satisfied for a cart/order.
    OrderNotFoundError:         Raised when an order lookup fails.
    OrderAlreadyCancelledError: Raised when cancelling an already-cancelled order.

Notes:
    Update this module as your system adds new error cases to keep exception handling consistent.
"""

# Inventory-related
class OutOfStockError(Exception):
    """Raised when trying to reserve or purchase more stock than available."""
    pass


# Payment-related
class PaymentFailedError(Exception):
    """Raised when payment processing fails in the payment gateway."""
    pass


# Coupon/Discount-related
class InvalidCouponError(Exception):
    """Raised when a coupon is invalid, expired, or not applicable."""
    pass

class DiscountNotApplicableError(Exception):
    """Raised when discount conditions are not satisfied for a cart/order."""
    pass


# Order-related
class OrderNotFoundError(Exception):
    """Raised when trying to access or cancel a non-existent order."""
    pass

class OrderAlreadyCancelledError(Exception):
    """Raised when cancelling an already-cancelled order."""
    pass