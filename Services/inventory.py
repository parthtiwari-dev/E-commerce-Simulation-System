"""
Inventory Management Module

Purpose:
    Centralizes all product inventory operations for the e-commerce system.
    Tracks available stock, processes stock reservations/deductions, and supports restocking.
    Provides methods for querying, adding, updating, and validating product availability.
    Can trigger alerts for low stock and integrates with order placement/cancellation logic.

Key Responsibilities:
    - Maintain a mapping of product_id to Product objects (or inventory records).
    - Check availability before allowing customers to add items to carts/order.
    - Reserve/deduct stock on successful orders; release/restock on cancellations or returns.
    - Support bulk loading of products from configuration or files.
    - Generate low-stock alerts and interface with logging/reporting subsystems.

Example Methods:
    add_product(product): Add a new Product to inventory.
    remove_product(product_id): Remove a Product from inventory.
    is_in_stock(product_id, quantity): Check if sufficient stock exists.
    reserve_stock(product_id, quantity): Deduct stock for an order.
    release_stock(product_id, quantity): Replenish stock after cancellation/return.
    get_inventory_status(): Return a summary or detailed view of current inventory.
    get_low_stock_products(threshold): Return products with stock below threshold.

"""

# services/inventory.py

# services/inventory.py

from models.product import Product
from typing import Dict, List, Optional


# Stub logger for now if you do not have an actual logger utility
class LoggerStub:
    @staticmethod
    def info(msg):
        print(f"[LOG] {msg}")


logger = LoggerStub()


# Stub exception if custom one doesn't exist yet
class OutOfStockError(Exception):
    pass


class Inventory:
    def __init__(self, logger=logger):
        """Initializes the inventory with an empty product dictionary and optional logger."""
        self.products: Dict[int, Product] = {}
        self.logger = logger

    def add_product(self, product: Product):
        """Add or update a Product in inventory."""
        self.products[product.product_id] = product
        self.logger.info(f"Product added: {product}")

    def remove_product(self, product_id: int):
        """Remove a product from inventory."""
        if product_id in self.products:
            del self.products[product_id]
            self.logger.info(f"Product removed: {product_id}")

    def is_in_stock(self, product_id: int, quantity: int) -> bool:
        """Check if the requested quantity is in stock."""
        product = self.products.get(product_id)
        return product.is_in_stock(quantity) if product else False

    def reserve_stock(self, product_id: int, quantity: int) -> bool:
        """
        Deduct/reserve stock for an order.
        Raises OutOfStockError if insufficient stock.
        """
        product = self.products.get(product_id)
        if not product or not product.is_in_stock(quantity):
            raise OutOfStockError(
                f"{product_id} is out of stock or insufficient quantity"
            )
        product.deduct_stock(quantity)
        self.logger.info(f"Reserved {quantity} of {product_id}")
        return True

    def release_stock(self, product_id: int, quantity: int):
        """Restock inventory after cancellation/return."""
        product = self.products.get(product_id)
        if product:
            product.restock(quantity)
            self.logger.info(f"Released {quantity} back to {product_id}")

    def get_inventory_status(self) -> List[Dict]:
        """Return product summaries for all products in inventory."""
        return [product.get_info() for product in self.products.values()]

    def get_low_stock_products(self, threshold: int) -> List[Dict]:
        """Return list of products at or below the given stock threshold."""
        return [p.get_info() for p in self.products.values() if p.stock <= threshold]
