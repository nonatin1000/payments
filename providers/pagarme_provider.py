from typing import List
from strategy.payment.interfaces.provider_interface import Provider
import logging


class PagarMeProvider(Provider):
    @property
    def name(self) -> str:
        return "PagarMe"

    @property
    def supported_methods(self) -> List[str]:
        return ["pix", "credit_card", "boleto"]

    def process_payment(self, method: str, amount: float) -> bool:
        if method not in self.supported_methods:
            raise ValueError(f"Method {method} not supported by {self.name}.")

        logging.info(f"[{self.name}] Processing payment of ${amount:.2f} via {method}.")
        return True
