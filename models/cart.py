"""
Cart Class

Purpose:
    Represents a user's temporary shopping cart.
    Maintains the products and quantities selected before checkout,
    manages coupon application, and provides calculations for subtotals, totals,
    and cart review.

Attributes:
    cart_id: Unique identifier for this cart (int or string)
    user_id: Identifier for the user who owns the cart (int or string)
    items: Dictionary holding cart products and their quantities
           (e.g., {product_id: (Product object, quantity)})
    applied_coupons: List of Coupon objects currently applied to the cart
    created_at: Timestamp of when the cart was created (optional)
    updated_at: Timestamp for the cart's last modification (optional)

Methods:
    add_item(product, quantity): Add a product and quantity to the cart; increases quantity if already present
    remove_item(product): Remove a product from the cart completely
    update_quantity(product, new_quantity): Adjust the quantity for a given product; removes if quantity is zero or less
    clear(): Remove all items and coupons from the cart
    view_items(): Return/display a summary of current items, quantities, and subtotal
    apply_coupon(coupon): Attempt to apply a coupon to the cart if valid
    remove_coupon(coupon): Remove an applied coupon from the cart
    calculate_subtotal(): Calculate the price total of all items before discounts
    calculate_total(): Calculate final total after applying discounts/coupons
    list_coupons(): Display summary of coupons currently applied
    is_empty(): Return True if the cart has no items; False otherwise
    get_cart_info(): Return a complete overview of the cart: items, subtotal, coupons, and total
"""

from datetime import datetime
from product import Product


class Cart:

    def __init__(self, cart_id, user_id, items=None, applied_coupons=None, created_at=None, updated_at=None):
        self.cart_id = cart_id
        self.user_id = user_id
        self.items = items if items is not None else {}  # {product_id: (Product, quantity)}
        self.applied_coupons = applied_coupons if applied_coupons is not None else []
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else self.created_at

    def add_item(self, product, quantity):
        pid = product.product_id

        if pid in self.items:
            existing_product, existing_qty = self.items[pid]
            new_qty = existing_qty + quantity
            if new_qty <= 0:
                del self.items[pid]
            else:
                self.items[pid] = (product, new_qty)
        else:
            if quantity > 0:
                self.items[pid] = (product, quantity)
        # If quantity <= 0 and not already present, do nothing
        self.updated_at = datetime.now()

    def remove_item(self, product, quantity):
        self.add_item(product, -quantity)

    def update_quantity(self):
        pass

    def clear(self):
        pass
    def view_items(self):
        pass
    def apply_coupon(self, coupon):
        pass
    def remove_coupon(self, coupon):
        pass
    def calculate_subtotal(self):
        pass
    def calculate_total():
        pass    
    def list_coupons():
        pass
    def is_empty():
        pass
    def get_cart_info():
        pass
    