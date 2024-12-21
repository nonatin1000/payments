from typing import List
from interfaces.provider_interface import Provider
import logging


class MercadoPagoProvider(Provider):
    @property
    def name(self) -> str:
        return "MercadoPago"

    @property
    def supported_methods(self) -> List[str]:
        return ["pix", "credit_card", "boleto"]

    def process_payment(self, payment_method: str, amount: float) -> bool:
        if payment_method not in self.supported_methods:
            raise ValueError(f"Method {payment_method} not supported by {self.name}.")

        logging.info(
            f"[{self.name}] Processing payment of ${amount:.2f} via {payment_method}."
        )
        # Simulating intentional failure for 'credit_card'
        if payment_method == "credit_card":
            raise Exception("Method credit_card not supported by MercadoPago.")
        return True
