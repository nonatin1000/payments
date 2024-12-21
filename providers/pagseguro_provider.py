from typing import List
from interfaces.provider_interface import Provider
import logging


class PagSeguroProvider(Provider):
    @property
    def name(self) -> str:
        return "PagSeguro"

    @property
    def supported_methods(self) -> List[str]:
        return ["pix", "credit_card", "boleto"]

    def process_payment(self, method: str, amount: float) -> bool:
        if method not in self.supported_methods:
            raise ValueError(f"Method {method} not supported by {self.name}.")

        logging.info(f"[{self.name}] Processing payment of ${amount:.2f} via {method}.")
        return True
