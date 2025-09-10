class User:
    def __init__(self, user_id, name, email, cart=None, orders=None, loyalty_points=0):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.cart = cart  # Should be a Cart object or None
        self.orders = orders if orders is not None else []  # List of Order objects
        self.loyalty_points = loyalty_points  # Optional, defaults to 0

    def add_to_cart(self,product, quantity):
        self.product = product
        self.quantity = quantity
    
    def remove_from_cart(self,product):
        self.product = product
    
    def view_cart(self, product):
        self.product = product
        print(product)
    