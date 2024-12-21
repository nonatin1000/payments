from typing import List
from interfaces.payment_strategy import PaymentStrategy
import logging


class CreditCardPayment(PaymentStrategy):
    @property
    def supported_methods(self) -> List[str]:
        return ["credit_card"]

    @property
    def payment_method(self) -> str:
        return "credit_card"

    @property
    def provider_name(self) -> str:
        return self.provider.name

    def process_payment(self, payment_method: str, amount: float) -> bool:
        logging.info(
            f"Starting credit card payment of R$ {amount:.2f} with provider {self.provider.name}."
        )
        return self.provider.process_payment(payment_method, amount)

    def pay(self, amount: float):
        self.process_payment(self.payment_method, amount)
