"""
Discount and Promotion Logic Module

Purpose:
    Centralizes all advanced discount and promotion logic for the e-commerce system.
    Applies discount rules, manages promotional campaigns, and enables stacking,
    exclusivity, or category-specific discounts beyond individual coupon objects.

Key Responsibilities:
    - Manage global or campaign-wide discounts in addition to per-coupon rules.
    - Evaluate eligibility for multiple simultaneous promotions (e.g., buy-one-get-one).
    - Handle stacking, mutual exclusivity, or priority of discounts.
    - Efficiently compute best applicable discounts for each cart or order.
    - Provide interfaces for adding, updating, or querying active discounts and promotions.

Example Methods:
    apply_discounts(cart): Evaluates and applies all valid discounts/coupons to a cart.
    is_eligible(cart, discount): Checks if a cart/order meets the criteria for a discount.
    add_discount(discount_rule): Adds a new discount or promotion to the system.
    get_active_discounts(): Returns current valid discounts/promotions.

Notes:
    Use this module if business requirements include system-wide sales,
    vendor-funded promotions, or complex stacking rules not handled by Coupon objects.
"""
"""
Discount and Promotion Logic Module
(Put the earlier docstring here!)
"""

from models.cart import Cart
from models.coupon import Coupon
from typing import List, Dict, Any, Optional

# Example discount rule structure
class DiscountRule:
    def __init__(self, name: str, description: str, discount_type: str, value: float, min_order_value: float = 0.0):
        self.name = name
        self.description = description
        self.discount_type = discount_type  # "fixed", "percentage", etc.
        self.value = value
        self.min_order_value = min_order_value

    def is_eligible(self, cart: Cart) -> bool:
        return cart.calculate_subtotal() >= self.min_order_value

    def get_discount(self, cart: Cart) -> float:
        if not self.is_eligible(cart):
            return 0.0
        if self.discount_type == "fixed":
            return min(self.value, cart.calculate_subtotal())
        elif self.discount_type == "percentage":
            return round(cart.calculate_subtotal() * (self.value / 100), 2)
        return 0.0

# Main discount manager (manages rules & coupons)
class DiscountManager:
    def __init__(self):
        self.discounts: List[DiscountRule] = []
        self.coupons: List[Coupon] = []

    def add_discount(self, discount: DiscountRule):
        self.discounts.append(discount)

    def apply_discounts(self, cart: Cart) -> float:
        """
        Calculates the maximum applicable discount (from rules + coupons)
        This can be customized for stacking/not stacking logic.
        """
        total_discount = 0
        # Apply all discount rules (stacking is just a sum here)
        for discount in self.discounts:
            total_discount += discount.get_discount(cart)
        # Apply all valid coupons
        for coupon in cart.applied_coupons:
            total_discount += coupon.get_discount(cart)
        return total_discount

    def get_active_discounts(self) -> List[DiscountRule]:
        """Returns a list of all active discount promotions."""
        return self.discounts

    def is_eligible(self, cart: Cart, discount: DiscountRule) -> bool:
        """Checks if a specific discount rule or coupon is valid for this cart."""
        return discount.is_eligible(cart)

