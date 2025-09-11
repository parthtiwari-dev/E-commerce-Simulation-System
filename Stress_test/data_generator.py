"""
Random Data Generator for Stress Testing

Purpose:
    Provides helper functions to generate synthetic users, products, and carts for high-volume testing
    of the e-commerce system. Enables simulation of realistic, large-scale e-commerce scenarios.

Key Responsibilities:
    - Generate a configurable number of sample users, products, and orders with randomized attributes.
    - Support batch creation to populate the system prior to stress test runs.
    - Optionally, support seeding for reproducible tests.

Example Methods:
    generate_products(n):        Returns a list of n Product objects with random details.
    generate_users(n):           Returns a list of n User objects.
    generate_carts(users, ...):  Returns carts filled by users with randomized selections.

Notes:
    Used only for bulk/system stress testing—never in production logic.
"""

import random
import string
from models.product import Product
from models.user import User
from models.cart import Cart
from models.coupon import Coupon


def random_string(length=6):
    """Generate a random string of given length."""
    return "".join(random.choices(string.ascii_letters, k=length))


def generate_products(n=10):
    """Generate n sample products with random attributes."""
    categories = ["Electronics", "Clothing", "Books", "Home", "Toys"]
    products = []
    for i in range(1, n + 1):
        name = f"{random.choice(categories)}-{random_string(4)}"
        price = round(random.uniform(100, 50000), 2)
        stock = random.randint(1, 50)
        category = random.choice(categories)
        product = Product(
            product_id=i, name=name, price=price, stock=stock, category=category
        )
        products.append(product)
    return products


def generate_users(n=5):
    """Generate n sample users with random details."""
    users = []
    for i in range(1, n + 1):
        name = f"User-{random_string(5)}"
        email = f"{name.lower()}@example.com"
        user = User(user_id=i, name=name, email=email)
        users.append(user)
    return users


def generate_carts(users, products, max_items=3):
    """Generate a cart for each user with random product selections."""
    carts = []
    for user in users:
        cart = Cart(user_id=user.user_id, cart_id=f"CART-{user.user_id}")
        chosen = random.sample(products, k=random.randint(1, max_items))
        for product in chosen:
            qty = random.randint(1, 2)
            cart.add_item(product, qty)
        carts.append(cart)
    return carts


def generate_coupons(n=3):
    """Generate n sample coupons with random discount rules."""
    coupons = []
    for i in range(1, n + 1):
        code = f"COUPON{i}{random_string(2).upper()}"
        discount_type = random.choice(["fixed", "percentage"])
        value = (
            random.randint(50, 5000)
            if discount_type == "fixed"
            else random.randint(5, 20)
        )
        min_order_value = random.randint(0, 2000)
        coupon = Coupon(
            code=code,
            description=f"{value}{'%' if discount_type=='percentage' else '₹'} OFF",  # 👈 yeh add kar diya
            discount_type=discount_type,
            discount_value=value,
            min_order_value=min_order_value,
        )
        coupons.append(coupon)
    return coupons


# utils/data_generator.py

if __name__ == "__main__":
    products = generate_products(5)
    users = generate_users(3)
    coupons = generate_coupons(2)

    print("\nGenerated Products:")
    for p in products:
        print(p.get_info())

    print("\nGenerated Users:")
    for u in users:
        print(u.get_profile())

    print("\nGenerated Coupons:")
    for c in coupons:
        print(c.get_info())
