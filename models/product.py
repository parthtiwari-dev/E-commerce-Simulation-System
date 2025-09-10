"""
Product Class

Purpose:
    Represents a unique item that can be purchased.
    Holds product data and provides methods for inventory control.

Attributes:
    product_id: Unique int/str identifier for the product
    name: Name of the product
    description: Short description (optional)
    price: Price per unit (float/int)
    stock: Current available stock (int)
    category: Optional product category (str)

Methods:
    deduct_stock(quantity): Reduce the available stock by quantity
    restock(quantity): Increase available stock by quantity
    is_in_stock(quantity): Check if enough stock exists for a request
    set_price(new_price): Update the current product price
    get_info(): Return product information for logs/display
"""

class Product:
    def __init__(self, product_id, name, price, stock , description = "", category = "General"):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        self.description = description
        self.category = category

    def deduct_stock(self , quantity:int) -> bool:
        if quantity <= self.stock:
            self.stock -= quantity
            return True
        return False

    def restock(self,quantity:int):
        self.stock += quantity

    def is_in_stock(self, quantity:int) -> bool:
        return quantity<= self.stock

    def set_price(self,new_price: float):
        self.price = new_price

    def get_info(self):
        return{
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
        }
    def __repr__(self):
        return f"<Product {self.name} (₹{self.price}, stock={self.stock})>"  


