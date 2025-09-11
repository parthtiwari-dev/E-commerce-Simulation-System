from Services.inventory import Inventory
from Services.payment_gateway import PaymentProcessor
from Services.order_services import OrderServices
from Stress_test.data_generator import (
    generate_products,
    generate_users,
    generate_coupons,
)
from Utils.logger import info, warning
import random
from config import DEFAULT_PRODUCT_STOCK, PAYMENT_SUCCESS_RATE



def main():
    # 1. Generate initial data
    products = generate_products(20)
    users = generate_users(5)
    coupons = generate_coupons(3)

    # 2. Initialize services
    inventory = Inventory()
    for product in products:
        inventory.add_product(product)

    payment_gateway = PaymentProcessor(success_rate=0.95)
    order_services = OrderServices(inventory, payment_gateway)

    # 3. Example simulation: user actions
    print("\n--- Product List ---")
    for p in products[:10]:  # show only first 10
        print(p.get_info())

    user = random.choice(users)
    print(f"\nSimulating actions for user: {user.get_profile()}")

    # 4. Create a cart and add random products
    from models.cart import Cart

    cart = Cart(cart_id=f"CART-{user.user_id}", user_id=user.user_id)

    for _ in range(3):
        prod = random.choice(products)
        qty = random.randint(1, min(prod.stock, 3))
        cart.add_item(prod, qty)
    print("\nCart items:", {pid: (p.name, q) for pid, (p, q) in cart.items.items()})

    # 5. Apply a coupon randomly
    if coupons and random.random() < 0.5:
        cart.apply_coupon(random.choice(coupons))
        print("Coupon applied!")

    # 6. Checkout
    payment_info = {"method": "credit_card", "card_number": "12341234", "cvv": "555"}
    order = order_services.submit_order(user, cart, payment_info)
    if order:
        print(
            f"\nOrder placed successfully! Order ID: {order.order_id}, Total: {order.total}"
        )
    else:
        print("\nOrder failed!")

    # 7. View order history
    print("\nUser Order History:")
    for o in user.order_history:
        print(o.get_order_info())


if __name__ == "__main__":
    main()
