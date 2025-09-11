"""
Order Class

Purpose:
    Represents a finalized customer order created from a shopping cart at checkout.
    Stores transaction details, handles order status tracking, order summary generation,
    and captures the state of the cart at time of order.

Attributes:
    order_id: Unique identifier for this order (int or string)
    user_id: Identifier for the user who placed the order (int or string)
    items: Dictionary or list holding purchased products and their quantities
           (e.g., {product_id: (Product object, quantity)})
    applied_coupons: List of Coupon objects used for this order
    subtotal: Total price of all items before discounts (float)
    total: Final order total after applying discounts/coupons (float)
    status: Current status of the order (e.g., "Placed", "Confirmed", "Shipped", "Delivered", "Cancelled")
    order_date: Timestamp of when the order was placed
    (Optional) shipping_address: Delivery address for the order
    (Optional) payment_info: Record of payment method or transaction details
    (Optional) order_notes: Freeform notes (e.g., delivery instructions)

Methods:
    __init__(...): Initialize an Order from parameters or a Cart instance
    update_status(new_status): Change the current order status
    get_order_info(): Return a summary of the order as a dictionary (order slip/receipt)
    __str__(): Display a concise summary of the order for logs/reports
    (Optional) cancel_order(): Change status to "Cancelled" and handle refund logic if needed
    (Optional) add_order_note(note): Attach administrative or customer note
"""

from datetime import datetime
from .cart import Cart
from .product import Product


class Order:
    def __init__(
        self,
        order_id,
        user_id,
        items,
        subtotal,
        total,
        applied_coupons,
        order_date,
        status="Placed",
        shipping_address=None,
        payment_info=None,
        order_notes=None,
    ):
        self.order_id = order_id
        self.user_id = user_id
        self.items = items
        self.subtotal = subtotal
        self.total = total
        self.applied_coupons = applied_coupons
        self.order_date = order_date
        self.status = status
        self.shipping_address = shipping_address
        self.payment_info = payment_info
        self.order_notes = order_notes

    @classmethod
    def from_cart(
        cls,
        order_id,
        cart,
        status="Placed",
        shipping_address=None,
        payment_info=None,
        order_notes=None,
    ):
        """
        Alternate constructor: create an Order from a Cart object,
        copying over products, coupons, totals etc.
        """
        return cls(
            order_id=order_id,
            user_id=cart.user_id,
            items=cart.items.copy(),
            subtotal=cart.calculate_subtotal(),
            total=cart.calculate_total(),
            applied_coupons=cart.applied_coupons.copy(),
            order_date=datetime.now(),
            status=status,
            shipping_address=shipping_address,
            payment_info=payment_info,
            order_notes=order_notes,
        )

    def update_status(self, new_status):
        self.status = new_status

    def get_order_info(self):
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
            "order_id": self.order_id,
            "user_id": self.user_id,
            "products": products,
            "applied_coupons": [
                coupon.code if hasattr(coupon, "code") else str(coupon)
                for coupon in self.applied_coupons
            ],
            "subtotal": self.subtotal,
            "total": self.total,
            "order_date": self.order_date,
            "status": self.status,
            "shipping_address": self.shipping_address,
            "payment_info": self.payment_info,
            "order_notes": self.order_notes,
        }


    def __str__(self):
        return (
            f"<Order {self.order_id} | User {self.user_id} | "
            f"{len(self.items)} items | Total: ₹{self.total:.2f} | Status: {self.status}>"
        )
