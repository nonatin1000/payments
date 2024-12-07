from strategy.payment.interfaces.payment_strategy import PaymentStrategy
import logging


class Checkout:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        """
        Sets the payment strategy.
        """
        self._strategy = strategy

    def pay(self, amount: float):
        """
        Executes the payment using the selected strategy.
        """
        logging.info(f"Starting payment of ${amount:,.2f}.")
        self._strategy.pay(amount)
