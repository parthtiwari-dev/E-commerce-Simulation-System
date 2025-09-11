"""
Logger Utility Module

Purpose:
    Provides a centralized logging utility for the e-commerce system.
    Wraps Python’s built-in 'logging' module to ensure consistency across all modules.
    Supports logging of informational messages, warnings, errors,
    and optionally to different outputs (stdout, file, etc.) with timestamps.

Key Responsibilities:
    - Standardize log message formats across all services and models.
    - Include timestamps and log levels (INFO, WARNING, ERROR, DEBUG).
    - (Optional) Save logs to files for persistent audit trails or debugging.
    - Make error tracking and monitoring easier during development and testing.

Example Methods:
    info(msg):     Log a general system action or event.
    warning(msg):  Log a warning condition (non-fatal issues).
    error(msg):    Log an error, exception, or failure scenario.
    debug(msg):    (Optional) Log detailed trace/debug info for developers.

Notes:
    - All services (PaymentGateway, OrderServices, Inventory, DiscountManager, etc.)
      should import and use this logger for consistent output.
    - Update configuration (format, file handlers) here to propagate everywhere.
"""
import logging

# Configure logger only once
logger = logging.getLogger("ecommerce")
if not logger.hasHandlers():  # Prevent duplicate handlers if re-imported
    logger.setLevel(logging.DEBUG)  # Capture all levels, handlers can filter
    handler = logging.StreamHandler()  # Console output
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Utility functions (simple wrappers)
def info(msg):
    logger.info(msg)

def warning(msg):
    logger.warning(msg)

def error(msg):
    logger.error(msg)

def debug(msg):
    logger.debug(msg)
