from typing import List
from strategy.payment.interfaces.provider_interface import Provider


class PaymentStrategy(Provider):
    def __init__(self, provider: Provider):
        self.provider = provider

    @property
    def name(self) -> str:
        return self.provider.name

    @property
    def supported_methods(self) -> List[str]:
        raise NotImplementedError("Este método deve ser implementado pelas subclasses.")

    def process_payment(self, payment_method: str, amount: float) -> bool:
        raise NotImplementedError("Este método deve ser implementado pelas subclasses.")

    @property
    def payment_method(self) -> str:
        raise NotImplementedError("Este método deve ser implementado pelas subclasses.")

    def pay(self, amount: float):
        raise NotImplementedError("Este método deve ser implementado pelas subclasses.")
