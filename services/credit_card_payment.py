from typing import List
from strategy.payment.interfaces.payment_strategy import PaymentStrategy


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
        print(
            f"Iniciando pagamento Cartão de Crédito de R$ {amount:.2f} com o provider {self.provider.name}."
        )
        return self.provider.process_payment(payment_method, amount)

    def pay(self, amount: float):
        self.process_payment(self.payment_method, amount)
