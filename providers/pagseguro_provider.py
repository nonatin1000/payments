from typing import List
from strategy.payment.interfaces.provider_interface import Provider


class PagSeguroProvider(Provider):
    @property
    def name(self) -> str:
        return "PagSeguro"

    @property
    def supported_methods(self) -> List[str]:
        return ["pix", "credit_card", "boleto"]

    def process_payment(self, payment_method: str, amount: float) -> bool:
        if payment_method not in self.supported_methods:
            raise ValueError(f"Método {payment_method} não suportado por {self.name}.")

        print(
            f"[{self.name}] Processando pagamento de R$ {amount:.2f} via {payment_method}."
        )
        return True
