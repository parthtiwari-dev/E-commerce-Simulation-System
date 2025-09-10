# test_order_services.py

from models.user import User
from models.product import Product
from models.cart import Cart
from Services.inventory import Inventory
from Services.payment_gateway import PaymentProcessor
from Services.order_services import OrderServices

# -------------------------------
# Step 1: Setup Inventory
# -------------------------------
inventory = Inventory()
p1 = Product(product_id=1, name="Laptop", price=50000, stock=5, category="Electronics")
p2 = Product(product_id=2, name="Mouse", price=500, stock=10, category="Electronics")
inventory.add_product(p1)
inventory.add_product(p2)

# -------------------------------
# Step 2: Setup Payment Processor
# -------------------------------
payment_processor = PaymentProcessor(success_rate=0.8)  # 80% success chance

# -------------------------------
# Step 3: Setup Order Services
# -------------------------------
order_services = OrderServices(inventory, payment_processor)

# -------------------------------
# Step 4: Setup User & Cart
# -------------------------------
user = User(user_id=1, name="Parth", email="parth@example.com")
cart = Cart(cart_id=101, user_id=user.user_id)

cart.add_item(p1, 1)  # Add 1 Laptop
cart.add_item(p2, 2)  # Add 2 Mice

payment_info = {
    "method": "credit_card",
    "card_number": "1234123412341234",
    "cvv": "123"
}

# -------------------------------
# Step 5: Try placing an order
# -------------------------------
print("\n--- Attempting to place order ---")
order = order_services.submit_order(user, cart, payment_info)
if order:
    print(f"Order Placed Successfully! Order ID: {order.order_id}")
else:
    print("Order Failed!")

# -------------------------------
# Step 6: Try cancelling the order
# -------------------------------
if order:
    print("\n--- Attempting to cancel order ---")
    cancelled = order_services.cancel_order(user, order.order_id)
    print(f"Cancelled: {cancelled}")

# -------------------------------
# Step 7: Show User Orders
# -------------------------------
print("\n--- User Order History ---")
for o in order_services.get_orders_for_user(user):
    print(o)

# -------------------------------
# Step 8: Show Inventory Status
# -------------------------------
print("\n--- Inventory Status ---")
for info in inventory.get_inventory_status():
    print(info)
