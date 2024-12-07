from abc import ABC, abstractmethod
from typing import List


class Provider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Provider name (e.g., PagSeguro, MercadoPago).
        """
        pass

    @property
    @abstractmethod
    def supported_methods(self) -> List[str]:
        """
        List of supported payment methods (e.g., ['pix', 'credit_card']).
        """
        pass

    @abstractmethod
    def process_payment(self, method: str, amount: float) -> bool:
        """
        Processes the payment using the specified method and amount.

        :param method: Payment method (e.g., 'pix').
        :param amount: Payment amount.
        :return: True if the payment was successful, False otherwise.
        """
        pass
