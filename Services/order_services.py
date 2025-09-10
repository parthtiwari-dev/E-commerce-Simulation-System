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

# Stub logger (replace with your real logger later)
class LoggerStub:
    @staticmethod
    def info(msg):
        print(f"[LOG] {msg}")

logger = LoggerStub()

class OrderServices:
    def __init__(self, inventory: Inventory, payment_gateway: PaymentProcessor, logger=logger):
        self.inventory = inventory
        self.payment_gateway = payment_gateway
        self.logger = logger

    def submit_order(self, user: User, cart: Cart, payment_info: Dict[str, Any]) -> Order | None:
        """
        Full checkout orchestration:
        1. Reserve inventory for all cart items
        2. Process payment
        3. Create and store Order
        4. Rollback stock if payment fails
        """
        if not cart.items:
            self.logger.info("Cart is empty, cannot submit order.")
            return None

        reserved = []
        try:
            # Step 1: Reserve stock
            for pid, (product, qty) in cart.items.items():
                self.inventory.reserve_stock(pid, qty)
                reserved.append((pid, qty))

            # Step 2: Process payment
            total_amount = cart.calculate_subtotal()
            order_preview = Order.from_cart("preview", cart)  # for payment purposes
            payment_ref = self.payment_gateway.process_payment(user, order_preview, payment_info)

            # Step 3: Create actual order
            order_id = f"ORD-{user.user_id}-{len(user.order_history)+1}"
            order = Order.from_cart(order_id, cart)
            order.payment_ref = payment_ref
            order.status = "Paid"
            user.order_history.append(order)

            self.logger.info(f"Order {order_id} placed successfully for User {user.user_id}")
            return order

        except (OutOfStockError, PaymentFailedError) as e:
            # Rollback reserved stock
            for pid, qty in reserved:
                self.inventory.release_stock(pid, qty)
            self.logger.info(f"Order failed for User {user.user_id}: {e}")
            return None

    def cancel_order(self, user: User, order_id: str) -> bool:
        """
        Cancel an order and release inventory.
        Optionally, trigger refund via PaymentProcessor.
        """
        order = next((o for o in user.order_history if o.order_id == order_id), None)
        if not order:
            self.logger.info(f"Order {order_id} not found for User {user.user_id}")
            return False
        if order.status == "Cancelled":
            self.logger.info(f"Order {order_id} already cancelled")
            return False

        order.update_status("Cancelled")
        for pid, (product, qty) in order.items.items():
            self.inventory.release_stock(pid, qty)

        # Optionally: refund via PaymentProcessor
        if hasattr(order, "payment_ref"):
            try:
                self.payment_gateway.refund_payment(order.payment_ref, order.total)
            except Exception as e:
                self.logger.info(f"Refund failed for Order {order_id}: {e}")

        self.logger.info(f"Order {order_id} cancelled successfully")
        return True

    def get_orders_for_user(self, user: User) -> List[Dict]:
        """Return summaries of all orders for a user."""
        return [order.get_order_info() for order in user.order_history]
