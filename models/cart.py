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
    remove_item(product, quantity): Remove a quantity of a product from the cart
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
    def __init__(
        self,
        cart_id,
        user_id,
        items=None,
        applied_coupons=None,
        created_at=None,
        updated_at=None,
    ):
        self.cart_id = cart_id
        self.user_id = user_id
        self.items = (
            items if items is not None else {}
        )  # {product_id: (Product, quantity)}
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
        self.updated_at = datetime.now()

    def remove_item(self, product, quantity):
        self.add_item(product, -quantity)

    def update_quantity(self, product, new_quantity):
        pid = product.product_id
        if pid in self.items:
            if new_quantity > 0:
                self.items[pid] = (product, new_quantity)
            else:
                del self.items[pid]
            self.updated_at = datetime.now()

    def clear(self):
        self.items.clear()
        self.applied_coupons.clear()
        self.updated_at = datetime.now()

    def view_items(self):
        if not self.items:
            print("Cart is empty.")
            return
        print(f"{'Product':<20} {'Qty':<5} {'Unit Price':<12} {'Subtotal':<10}")
        print("-" * 55)
        total = 0
        for pid, (product, quantity) in self.items.items():
            subtotal = product.price * quantity
            total += subtotal
            print(
                f"{product.name:<20} {quantity:<5} ₹{product.price:<12.2f} ₹{subtotal:<10.2f}"
            )
        print("-" * 55)
        print(f"{'Total':<20} {'':<5} {'':<12} ₹{total:<10.2f}")

    def apply_coupon(self, coupon):
        """
        Applies coupon if not already applied.
        Assumes coupon is a valid object and validation is handled elsewhere.
        """
        if coupon not in self.applied_coupons:
            self.applied_coupons.append(coupon)
            self.updated_at = datetime.now()
            print(
                f"Coupon {coupon.code if hasattr(coupon, 'code') else coupon} applied."
            )
        else:
            print(
                f"Coupon {coupon.code if hasattr(coupon, 'code') else coupon} is already applied."
            )

    def remove_coupon(self, coupon):
        """
        Removes the specified coupon if it's currently applied.
        """
        if coupon in self.applied_coupons:
            self.applied_coupons.remove(coupon)
            self.updated_at = datetime.now()
            print(
                f"Coupon {coupon.code if hasattr(coupon, 'code') else coupon} removed."
            )
        else:
            print(
                f"Coupon {coupon.code if hasattr(coupon, 'code') else coupon} is not in the cart."
            )

    def calculate_subtotal(self):
        return sum(
            product.price * quantity for product, quantity in self.items.values()
        )

    def calculate_total(self):
        subtotal = self.calculate_subtotal()
        total_discount = 0
        for coupon in self.applied_coupons:
            if hasattr(coupon, "get_discount"):
                total_discount += coupon.get_discount(self)
            elif hasattr(coupon, "discount_value"):
                total_discount += coupon.discount_value
            else:
                total_discount += float(coupon)
        return max(0, subtotal - total_discount)

    def list_coupons(self):
        if not self.applied_coupons:
            print("No coupons applied.")
        else:
            print("Applied coupons:")
            for coupon in self.applied_coupons:
                code = coupon.code if hasattr(coupon, "code") else str(coupon)
                print(f"- {code}")

    def is_empty(self):
        return len(self.items) == 0

    def get_cart_info(self):
        """
        Returns a summary dict of the cart's contents and totals.
        """
        products = [
            {
                "product_id": product.product_id,
                "name": product.name,
                "quantity": quantity,
                "unit_price": product.price,
                "subtotal": product.price * quantity,
            }
            for product, quantity in self.items.values()
        ]
        return {
            "cart_id": self.cart_id,
            "user_id": self.user_id,
            "products": products,
            "applied_coupons": [
                coupon.code if hasattr(coupon, "code") else str(coupon)
                for coupon in self.applied_coupons
            ],
            "subtotal": self.calculate_subtotal(),
            "total": self.calculate_total(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __str__(self):
        return f"<Cart {self.cart_id} - {len(self.items)} items, Total: ₹{self.calculate_total():.2f}>"
