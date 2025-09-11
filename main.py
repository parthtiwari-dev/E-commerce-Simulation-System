"""
Comprehensive E-commerce System Test Script

Covers:
- Product, Cart, Coupon, User, and Order models
- Inventory and Payment services
- Discount manager and transaction context
- End-to-end checkout, cancellation, and error handling
"""

from models.product import Product
from models.cart import Cart
from models.coupon import Coupon
from models.user import User
from models.order import Order
from Services.inventory import Inventory
from Services.payment_gateway import PaymentProcessor
from Services.order_services import OrderServices
from Services.discount import DiscountManager, DiscountRule
from Services.transaction import TransactionContext
from Utils.logger import logger
from Utils.exceptions import (OutOfStockError, PaymentFailedError)
import random

def run_all_tests():
    # 1. Setup Products
    laptop = Product(product_id=1, name="Laptop", price=50000, stock=5, category="Electronics")
    book = Product(product_id=2, name="Book", price=500, stock=10, category="Books")
    mug = Product(product_id=3, name="Mug", price=250, stock=20, category="Home")

    # 2. Setup Inventory and Load Products
    inventory = Inventory()
    inventory.add_product(laptop)
    inventory.add_product(book)
    inventory.add_product(mug)

    # 3. Setup User and Cart
    user = User(user_id=101, name="Alice", email="alice@example.com", address="42 Demo Lane")
    cart = Cart(cart_id="C101", user_id=user.user_id)
    cart.add_item(laptop, 1)
    cart.add_item(book, 2)

    # 4. Setup Coupon and Discount
    coupon = Coupon(
        code="EVERY10",
        description="10% off Electronics above ₹30,000",
        discount_type="percentage",
        discount_value=10,
        min_order_value=30000,
        applicable_categories=["Electronics"]
    )
    cart.apply_coupon(coupon)

    discount_manager = DiscountManager()
    special_discount = DiscountRule(name="Book50", description="₹50 off books", discount_type="fixed", value=50, min_order_value=100)
    discount_manager.add_discount(special_discount)

    # 5. Setup Payment Processor and OrderServices
    payment_gateway = PaymentProcessor(success_rate=1.0)  # Always succeed for this demo
    order_services = OrderServices(inventory=inventory, payment_gateway=payment_gateway)

    # 6. Display Cart (Pre-Order)
    print("\n--- CART SUMMARY ---")
    cart.view_items()
    print("Cart coupons:", cart.applied_coupons)
    print("Discounts applied from manager:", discount_manager.apply_discounts(cart))

    # 7. Run Transactional Checkout Flow (with rollback capability)
    payment_info = {"method": "credit_card", "card_number": "1234567812345678", "cvv": "123"}
    print("\n--- PLACING ORDER ---")
    with TransactionContext() as t:
        try:
            # Attempt order submission through OrderServices (invokes inventory, payment, models)
            order = order_services.submit_order(user, cart, payment_info)
            if order:
                print("\n--- ORDER PLACED ---")
                print(order.get_order_info())
            else:
                print("Order failed!")
        except (OutOfStockError, PaymentFailedError) as e:
            t.add_rollback(lambda: print("Rollback would trigger here if needed"))
            print(f"[ERROR] {e}")

    # 8. Cancel Order and Restock
    order_id = user.order_history[0].order_id if user.order_history else None
    if order_id:
        print("\n--- CANCELLING ORDER ---")
        success = order_services.cancel_order(user, order_id)
        if success:
            print(f"Order {order_id} cancelled successfully.")
        else:
            print("Order cancellation failed.")

    # 9. Inventory check (post-flow)
    print("\n--- FINAL INVENTORY STATUS ---")
    for item in inventory.get_inventory_status():
        print(item)

    # 10. User order history and profile
    print("\n--- USER PROFILE & ORDER HISTORY ---")
    print(user.get_profile())
    print("Order history:", user.get_order_history())

if __name__ == '__main__':
    run_all_tests()
