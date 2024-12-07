import logging
from strategy.payment.interfaces.payment_strategy import PaymentStrategy
from strategy.payment.services.fallback_processor import FallbackProcessor


class CombinedPayment(PaymentStrategy):
    def __init__(self):
        self.payments = []

    def add_payment(self, payment_strategy: PaymentStrategy, proportion: float):
        """
        Adds a payment strategy.

        :param payment_strategy: Instance of PaymentStrategy.
        :param proportion: Proportion of the total amount for this payment.
        """
        if proportion < 0 or proportion > 1:
            raise ValueError("Proportion must be between 0 and 1.")
        self.payments.append({"strategy": payment_strategy, "proportion": proportion})

    def pay(self, total_amount: float):
        """
        Processes the payment using the combined strategies.

        :param total_amount: Total amount to be paid.
        """
        if not self.payments:
            raise ValueError("No payment strategy has been added.")

        logging.info(f"Combined payment of R$ {total_amount:,.2f} started.")
        pending_amount = total_amount

        # Group strategies by payment method
        strategies_by_method = self._group_strategies_by_method()
        fallback_processor = FallbackProcessor(strategies_by_method)

        # Process each payment method independently
        for payment in self.payments:
            if pending_amount <= 0:
                break

            pending_amount = self._process_payment(
                payment, total_amount, pending_amount
            )

        # Process pending balance with fallback across all payment methods
        if pending_amount > 0:
            result = fallback_processor.process(pending_amount)
            if result:
                pending_amount = 0

        # Check if the payment was completed
        if pending_amount > 0:
            self._handle_payment_failure(total_amount - pending_amount, total_amount)
        else:
            logging.info(
                f"Payment successfully completed. Total paid: R$ {total_amount:,.2f}."
            )

    def _process_payment(self, payment, total_amount, pending_amount):
        """
        Processes a payment attempt.

        :param payment: Configured payment strategy.
        :param total_amount: Total amount to be paid.
        :param pending_amount: Amount still pending.
        :return: Pending amount after the payment attempt.
        """
        strategy = payment["strategy"]
        proportion = payment["proportion"]
        amount_to_pay = total_amount * proportion

        if amount_to_pay == 0:
            return pending_amount

        try:
            logging.info(
                f"Attempting to pay R$ {amount_to_pay:,.2f} with {strategy.provider_name}."
            )
            strategy.pay(amount_to_pay)
            logging.info(f"R$ {amount_to_pay:,.2f} successfully processed.")
            return pending_amount - amount_to_pay
        except Exception as e:
            logging.error(
                f"Failed to process R$ {amount_to_pay:,.2f} with {strategy.provider_name}: {e}"
            )
            return pending_amount

    def _handle_payment_failure(self, total_paid, total_amount):
        """
        Handles failures to complete the payment.

        :param total_paid: Amount already processed.
        :param total_amount: Total expected amount.
        """
        logging.error(f"Could not complete the payment of R$ {total_amount:,.2f}.")
        logging.error(
            f"Reverting completed transactions. Total to be refunded: R$ {total_paid:,.2f}."
        )

    def _group_strategies_by_method(self):
        """
        Groups strategies by payment method.

        :return: Dictionary with payment methods as keys and strategies as values.
        """
        grouped = {}
        for payment in self.payments:
            strategy = payment["strategy"]
            method = strategy.payment_method
            if method not in grouped:
                grouped[method] = []
            grouped[method].append(strategy)
        return grouped

    @property
    def payment_method(self) -> str:
        return "COMBINED"

    @property
    def provider_name(self) -> str:
        return "MULTIPLE"
