from typing import List
from interfaces.provider_interface import Provider


class PaymentStrategy(Provider):
    def __init__(self, provider: Provider):
        self.provider = provider

    @property
    def name(self) -> str:
        return self.provider.name

    @property
    def supported_methods(self) -> List[str]:
        raise NotImplementedError("This method must be implemented by subclasses.")

    def process_payment(self, method: str, amount: float) -> bool:
        raise NotImplementedError("This method must be implemented by subclasses.")

    @property
    def payment_method(self) -> str:
        raise NotImplementedError("This method must be implemented by subclasses.")

    def pay(self, amount: float):
        raise NotImplementedError("This method must be implemented by subclasses.")
