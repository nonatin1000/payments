from abc import ABC, abstractmethod
from typing import List


class Provider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Nome do provedor (ex.: PagSeguro, MercadoPago).
        """
        pass

    @property
    @abstractmethod
    def supported_methods(self) -> List[str]:
        """
        Lista de métodos de pagamento suportados (ex.: ['pix', 'credit_card']).
        """
        pass

    @abstractmethod
    def process_payment(self, method: str, amount: float) -> bool:
        """
        Processa o pagamento usando o método e o valor especificados.

        :param method: Método de pagamento (ex.: 'pix').
        :param amount: Valor do pagamento.
        :return: True se o pagamento foi bem-sucedido, False caso contrário.
        """
        pass
