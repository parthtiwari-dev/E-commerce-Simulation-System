"""
Order Services Module

Purpose:
    Orchestrates end-to-end order processing in the e-commerce system.
    Handles cart validation, inventory reservation, payment processing,
    order creation, cancellation, refund, and user order queries.
    Centralizes business logic that spans multiple models and services.

Key Responsibilities:
    - Submit new orders: validate cart, reserve stock, process payment, create Order
    - Rollback inventory or handle payment failures as needed
    - Cancel or refund orders, releasing inventory and issuing refunds via the gateway
    - Provide order search/history functions for users or admins
    - Log key order events and errors for auditing and debugging

Example Methods:
    submit_order(user, cart, payment_info): Full checkout orchestration
    cancel_order(order_id): Handle order cancellation and inventory/payment updates
    get_orders_for_user(user_id): List all orders placed by a user

Notes:
    This is the business logic "glue" between models (User, Cart, Product, Order, Coupon)
    and cross-cutting services (Inventory, PaymentGateway, Logger).
    Use try/except and proper error handling for reliability.
"""

# --- Imports (use your project structure; add/move as needed) ---
# Services/order_services.py

from models.user import User
from models.cart import Cart
from models.order import Order
from Services.inventory import Inventory, OutOfStockError
from Services.payment_gateway import PaymentProcessor, PaymentFailedError
from typing import Dict, Any, List
from Utils.logger import logger


class OrderServices:
    def __init__(
        self, inventory: Inventory, payment_gateway: PaymentProcessor, logger=logger
    ):
        self.inventory = inventory
        self.payment_gateway = payment_gateway
        self.logger = logger
        self.orders = []  # track all orders globally

    def submit_order(
        self, user: User, cart: Cart, payment_info: Dict[str, Any]
    ) -> Order | None:
        if not cart.items:
            self.logger.info("Cart is empty, cannot submit order.")
            return None

        reserved = []
        try:
            # Reserve stock
            for pid, (product, qty) in cart.items.items():
                self.inventory.reserve_stock(pid, qty)
                reserved.append((pid, qty))

            # Process payment
            order_preview = Order.from_cart("preview", cart)
            payment_ref = self.payment_gateway.process_payment(
                user, order_preview, payment_info
            )

            # Create order
            order_id = f"ORD-{user.user_id}-{len(self.orders)+1}"
            order = Order.from_cart(order_id, cart)
            order.payment_ref = payment_ref
            order.status = "Paid"

            # Save order
            self.orders.append(order)
            user.order_history.append(order)

            self.logger.info(
                f"Order {order_id} placed successfully for User {user.user_id}"
            )
            return order

        except (OutOfStockError, PaymentFailedError) as e:
            # Rollback reserved stock
            for pid, qty in reserved:
                self.inventory.release_stock(pid, qty)
            self.logger.info(f"Order failed for User {user.user_id}: {e}")
            return None

    def cancel_order(self, user_id: int, order_id: str) -> bool:
        # Find the order in self.orders
        order = next(
            (o for o in self.orders if o.user_id == user_id and o.order_id == order_id),
            None,
        )
        if not order:
            self.logger.info(f"Order {order_id} not found for User {user_id}")
            return False
        if order.status == "Cancelled":
            self.logger.info(f"Order {order_id} already cancelled")
            return False

        order.status = "Cancelled"
        for pid, (product, qty) in order.items.items():
            self.inventory.release_stock(pid, qty)

        # Refund if payment exists
        if hasattr(order, "payment_ref"):
            try:
                self.payment_gateway.refund_payment(order.payment_ref, order.total)
            except Exception as e:
                self.logger.info(f"Refund failed for Order {order_id}: {e}")

        self.logger.info(f"Order {order_id} cancelled successfully")
        return True
