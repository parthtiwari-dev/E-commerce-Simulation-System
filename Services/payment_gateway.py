"""
Payment Gateway Simulation Module

Purpose:
    Simulates external payment processing for the e-commerce system.
    Provides methods for charging users, handling payment information, and returning
    payment success or failure status. Mimics real-world gateway behavior for credit card,
    debit card, wallet, or UPI transactions.

Key Responsibilities:
    - Validate payment information format.
    - Simulate payment approval, rejection, or timeout scenarios.
    - Integrate with order placement: only finalize an order after successful payment.
    - Log payment attempts, errors, and confirmations for audit/debug purposes.
    - Raise custom exceptions (e.g., PaymentFailedError) on failure.

Example Methods:
    process_payment(user, order, payment_info): Process and validate the payment for a given order.
    refund_payment(order, amount): Simulate refunding payment to a customer (optional).
    validate_payment_info(payment_info): Check if card/UPI/wallet info is well-formed.
    log_transaction(details): Log each payment event or error (optional).

Notes:
    This module simulates payment only—it does not connect to real banks or gateways.
    Failures can be forced/randomized to test downstream error handling and rollback logic.
"""
from models.user import User
from models.order import Order
from models.cart import Cart
from Utils.logger import logger                # For logging payment events (use a stub if not made yet)
from typing import Any, Dict                   # For type hints
import random                                 # To simulate payment outcome
from Utils.exceptions import PaymentFailedError
   



class PaymentProcessor:
    def __init__(self, success_rate=0.9):
        """
        success_rate: probability [0,1] that a payment will succeed
        """
        self.success_rate = success_rate
        logger(f"PaymentProcessor created with success_rate={self.success_rate}")

    def validate_payment_info(self, payment_info: Dict[str, Any]) -> bool:
        """
        Check if payment_info dictionary has minimally required fields.
        In real systems, validate card numbers, expiry, etc.
        """
        required = ["method", "card_number", "cvv"]  # Example for card payment
        for field in required:
            if field not in payment_info:
                logger(f"Validation failed: missing {field}")
                return False
        return True


    def process_payment(self, user: User, order: Order, payment_info: Dict[str, Any]) -> str:
        """
        Attempt to charge the user's payment method for the order amount.
        Returns a payment reference string or raises PaymentFailedError.
        """
        logger(f"Payment attempt: user={user.user_id}, order={order.order_id}, amt={order.total}")
        if not self.validate_payment_info(payment_info):
            logger("Validation failed: Incomplete or invalid payment info.")
            raise PaymentFailedError("Invalid payment information supplied.")

        # Simulate payment gateway (randomly fail some payments)
        if random.random() < self.success_rate:
            payment_id = f"PAY-{order.order_id}-{random.randint(1000,9999)}"
            logger(f"Payment succeeded: {payment_id}")
            return payment_id
        else:
            logger("Payment failed by gateway simulation.")
            raise PaymentFailedError("Payment gateway declined the transaction.")

    def refund_payment(self, payment_ref: str, amount: float):
        """
        Simulate refund for a given payment reference.
        """
        logger(f"Refund processed for {payment_ref}: amount={amount}")
        return True


