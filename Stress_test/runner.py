"""
Stress Test Runner Script

Purpose:
    Orchestrates mass operations (order placement, payment, cancellation, etc.)
    to simulate large user volume and identify system bottlenecks, race conditions, or performance issues.

Key Responsibilities:
    - Launch a configurable number of simulated checkouts/payment/cancellation in sequence or parallel.
    - Report timing, throughput statistics, and error rates under stress.
    - Exercise error handling, transaction safety, and system resilience.
    - Log major events and summary statistics for later analysis.

Example Methods:
    run_basic_stress_test():         Runs many random orders and reports outcome stats.
    run_concurrent_checkout_test():  (Optional) Launches operations in threads/processes for concurrency.
    print_summary():                 Prints aggregated results after test runs.

Notes:
    Only relevant for testing/benchmarking—should not be deployed in a real environment.
"""

import time
import random

from Stress_test.data_generator import (
    generate_products,
    generate_users,
    generate_carts,
    generate_coupons,
)
from Services.inventory import Inventory
from Services.payment_gateway import PaymentProcessor
from Services.order_services import OrderServices
from Utils.logger import info, warning, error


def run_stress_test(
    num_products=100,
    num_users=50,
    num_orders=200,
    max_cart_items=5,
    coupon_prob=0.4,
    payment_success_rate=0.95,
):
    # 1. Generate test data
    products = generate_products(num_products)
    users = generate_users(num_users)
    coupons = generate_coupons(5)

    # 2. Prepare services
    inventory = Inventory()
    for product in products:
        inventory.add_product(product)
    payment_gateway = PaymentProcessor(success_rate=payment_success_rate)
    order_services = OrderServices(inventory, payment_gateway)

    # 3. Run high-volume order workflow
    successes, failures = 0, 0
    placed_orders = []
    t0 = time.time()

    for i in range(num_orders):
        user = random.choice(users)
        cart = random.choice(generate_carts([user], products, max_cart_items))
        # Randomly apply coupon to some carts
        if coupons and random.random() < coupon_prob:
            cart.apply_coupon(random.choice(coupons))
        payment_info = {
            "method": "credit_card",
            "card_number": "12341234",
            "cvv": "555",
        }
        order = order_services.submit_order(user, cart, payment_info)
        if order:
            successes += 1
            placed_orders.append(order)
            info(f"[ORDER {i+1}] Success: {order.order_id}, Total: {order.total}")
        else:
            failures += 1
            warning(f"[ORDER {i+1}] Failed")
    t1 = time.time()

    # 4. Print summary stats
    print("\n--- STRESS TEST SUMMARY ---")
    print(f"Total orders attempted:   {num_orders}")
    print(f"Orders successfully placed: {successes}")
    print(f"Failed attempts:          {failures}")
    print(f"Total runtime:            {t1 - t0:.2f} seconds")
    if successes:
        avg_order_value = sum(o.total for o in placed_orders) / successes
        print(f"Avg order value:         ₹{avg_order_value:.2f}")
        print(f"Max order value:         ₹{max(o.total for o in placed_orders):.2f}")
        print(f"Min order value:         ₹{min(o.total for o in placed_orders):.2f}")

    # Optionally, test cancellation rate
    cancels = 0
    for order in random.sample(placed_orders, k=min(len(placed_orders), 20)):
        result = order_services.cancel_order(order.user, order.order_id)
        if result:
            cancels += 1
            info(f"Order {order.order_id} cancelled.")
    if cancels:
        print(f"Orders cancelled in test: {cancels}")

    print("\n--- Stress Test Complete ---")


if __name__ == "__main__":
    run_stress_test()
