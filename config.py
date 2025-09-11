"""
config.py

Central configuration for the E-commerce Simulation System.
Contains all tunable system constants for easy maintenance and experimentation.
"""

# --- Inventory & Product Config ---
DEFAULT_PRODUCT_STOCK = 20
INVENTORY_LOW_STOCK_THRESHOLD = 3

# --- Payment Gateway ---
PAYMENT_SUCCESS_RATE = 0.97           # 97% payments will succeed by default
PAYMENT_PROCESS_DELAY_SEC = 0         # Add >0 for demoing async/slow payment

# --- Discount & Coupon Settings ---
DEFAULT_COUPON_CODES = ["EVERY10", "BOOK50"]
SITEWIDE_DISCOUNT_PERCENT = 5         # 5% off everywhere, if enabled

# --- Stress Test Simulation ---
NUM_USERS_STRESS_TEST = 50
NUM_PRODUCTS_STRESS_TEST = 100
NUM_ORDERS_STRESS_TEST = 500
MAX_CART_ITEMS_PER_USER = 5
COUPON_PROBABILITY = 0.4              # 40% of checkouts will try applying coupon
STRESS_TEST_PAYMENT_SUCCESS_RATE = 0.95

# --- Logging ---
LOG_LEVEL = "INFO"                    # "DEBUG", "INFO", "WARNING", "ERROR"
LOG_FILE_PATH = "ecommerce_simulation.log"

# --- Miscellaneous ---
RANDOM_SEED = 42                      # Use for repeatable random test results
ENABLE_AUTO_REFUNDS = True
ENABLE_CONCURRENT_ORDERS = False      # For advanced simulation/workload

# --- Feature Flags / Toggles (Optional) ---
ENABLE_EMAIL_NOTIFICATIONS = False

# Add more as your project grows!
