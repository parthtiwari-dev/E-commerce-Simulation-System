"""
Coupon Class

Purpose:
    Represents a discount or promotional offer that can be applied to a cart or order.
    Supports percentage-based, fixed-amount, and conditional discounts.
    Handles coupon validation, discount calculation, and usage tracking.

Attributes:
    code: Unique string identifier for the coupon (e.g., "SAVE10")
    description: Human-readable description of the coupon (e.g., "10% off on orders above ₹1000")
    discount_type: Type of discount ("percentage", "fixed", etc.)
    discount_value: Value of the discount (e.g., 10 for 10% or 500 for ₹500 off)
    min_order_value: Minimum cart/order total required to apply the coupon (optional)
    valid_from: Datetime indicating when the coupon becomes active (optional)
    valid_until: Datetime after which the coupon is expired (optional)
    applicable_categories: List of product categories this coupon can be applied to (optional)
    max_uses: Total number of times this coupon can be used per customer or in total (optional)
    usage_count: Tracks number of times the coupon has been used (optional)
    (Optional) is_active: Boolean flag for internal deactivation

Methods:
    is_valid(cart): Checks if the coupon can be applied to the given cart (validity, order value, etc.)
    get_discount(cart): Calculates the discount amount for the given cart.
    apply(coupon, cart): Applies coupon logic to a cart (if not already applied).
    increment_usage(): Increments the coupon usage count.
    (Optional) deactivate(): Soft-deletes or disables the coupon.
    (Optional) can_be_used_by(user): Checks if a particular user is eligible.
"""

from datetime import datetime
from .cart import Cart


class Coupon:
    def __init__(
        self,
        code,
        description,
        discount_type,
        discount_value,
        min_order_value=0.0,
        valid_from=None,
        valid_until=None,
        applicable_categories=None,
        max_uses=None,
        is_active=True,
    ):
        self.code = code
        self.description = description
        self.discount_type = discount_type  # "fixed" or "percentage"
        self.discount_value = discount_value
        self.min_order_value = min_order_value
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.applicable_categories = applicable_categories or []
        self.max_uses = max_uses
        self.usage_count = 0  # Always starts at 0
        self.is_active = is_active

    def is_valid(self, cart):
        now = datetime.now()

        if not self.is_active:
            return False, "Coupon is not active."
        if self.valid_from and now < self.valid_from:
            return False, "Coupon not yet valid."
        if self.valid_until and now > self.valid_until:
            return False, "Coupon expired."
        if self.max_uses is not None and self.usage_count >= self.max_uses:
            return False, "Coupon max usage reached."
        if cart.calculate_subtotal() < self.min_order_value:
            return (
                False,
                f"Order value is below the minimum required ₹{self.min_order_value}.",
            )
        if self.applicable_categories:
            found = any(
                product.category in self.applicable_categories
                for product, quantity in cart.items.values()
            )
            if not found:
                return False, "No eligible products for this coupon."
        return True, "Coupon is valid."

    def get_discount(self, cart):
        is_valid, msg = self.is_valid(cart)
        if not is_valid:
            return 0.0
        subtotal = cart.calculate_subtotal()
        if self.discount_type == "fixed":
            return min(self.discount_value, subtotal)
        elif self.discount_type == "percentage":
            return round(subtotal * (self.discount_value / 100), 2)
        return 0.0

    def increment_usage(self):
        self.usage_count += 1

    def deactivate(self):
        self.is_active = False

    def __str__(self):
        return f"<Coupon {self.code}: {self.description} | {self.discount_type} {self.discount_value}>"
