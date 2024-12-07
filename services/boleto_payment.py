from typing import List

from strategy.payment.interfaces.payment_strategy import PaymentStrategy
import logging


class BoletoPayment(PaymentStrategy):
    @property
    def supported_methods(self) -> List[str]:
        return ["boleto"]

    @property
    def payment_method(self) -> str:
        return "boleto"

    @property
    def provider_name(self) -> str:
        return self.provider.name

    def process_payment(self, payment_method: str, amount: float) -> bool:
        logging.info(
            f"Starting Boleto payment of R$ {amount:.2f} with provider {self.provider.name}."
        )
        return self.provider.process_payment(payment_method, amount)

    def pay(self, amount: float):
        self.process_payment(self.payment_method, amount)
