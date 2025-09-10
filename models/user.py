"""
User Class

Purpose:
    Represents a customer/user in the e-commerce system.
    Manages user identity, profile information, addresses, cart, and order history.
    Provides methods to interact with the user's current cart and track placed orders.

Attributes:
    user_id: Unique identifier for the user (int or string)
    name: User's full name
    email: Contact email for the user
    (Optional) address: Default shipping/delivery address (could be a string or a dedicated Address object)
    current_cart: The user's active shopping cart (Cart object)
    order_history: List of previously completed Order objects
    (Optional) payment_methods: List of saved payment method info
    (Optional) phone: User's phone number

Methods:
    add_to_cart(product, quantity): Add a product and quantity to the user's current cart
    remove_from_cart(product, quantity): Remove a quantity of a product from the user's cart
    clear_cart(): Empty the user's current cart
    place_order(order_id, shipping_address=None, payment_info=None): Finalize the current cart as an Order and start a new cart
    get_order_history(): Return a list/summary of the user's past orders
    get_profile(): Return user's profile information as a dictionary
    (Optional) update_profile(**fields): Update name, email, or address info
    (Optional) add_payment_method(payment_info): Save a new payment method

"""

from models.cart import Cart
from models.order import Order
from models.product import Product
from datetime import datetime


class User:
    def __init__(self, user_id, name, email, address=None, phone=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.address = address
        self.phone = phone
        self.current_cart = Cart(
            cart_id=f"cart-{self.user_id}-{int(datetime.now().timestamp())}",
            user_id=self.user_id,
        )  # Active cart
        self.order_history = []  # List of Order objects
        self.payment_methods = []

    ## methods to manipulate cart
    def add_to_cart(self, product, quantity):
        self.current_cart.add_item(product, quantity)

    def remove_from_cart(self, product, quantity):
        self.current_cart.remove_item(product, quantity)

    def clear_cart(self):
        self.current_cart.clear()

    ## methods to place an order from the cart
    def place_order(
        self, order_id, shipping_address=None, payment_info=None, order_notes=None
    ):
        order = Order.from_cart(
            order_id=order_id,
            cart=self.current_cart,
            shipping_address=shipping_address or self.address,
            payment_info=payment_info,
            order_notes=order_notes,
        )
        self.order_history.append(order)
        # Create new empty cart with unique cart_id for the user
        from datetime import datetime

        self.current_cart = Cart(
            cart_id=f"cart-{self.user_id}-{int(datetime.now().timestamp())}",
            user_id=self.user_id,
        )

        return order

    ## profile and order history
    def get_profile(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone": self.phone,
        }

    def get_order_history(self):
        return [order.get_order_info() for order in self.order_history]

    # For Payments & Updates

    def add_payment_method(self, payment_info):
        self.payment_methods.append(payment_info)

    def update_profile(self, name=None, email=None, address=None, phone=None):
        if name:
            self.name = name
        if email:
            self.email = email
        if address:
            self.address = address
        if phone:
            self.phone = phone

    def __str__(self):
        return (
            f"<User {self.user_id}: {self.name} | Orders: {len(self.order_history)} | "
            f"Cart Items: {len(self.current_cart.items)}>"
        )
