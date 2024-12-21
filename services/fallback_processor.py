from typing import Dict, List, Optional
from contexts.payment_processor import PaymentProcessor
from interfaces.payment_strategy import PaymentStrategy
import logging


class FallbackProcessor:
    def __init__(self, strategies_by_method: Dict[str, List[PaymentStrategy]]):
        self.strategies_by_method = strategies_by_method
        self.failed_providers_by_method = (
            {}
        )  # Tracks failed providers by payment method

    def process(self, pending_amount: float) -> Optional[str]:
        """
        Processes the pending balance with fallback providers for all payment methods.
        Returns the name of the provider that approved the payment or None if all fail.
        """
        for method, strategies in self.strategies_by_method.items():
            if method in self.failed_providers_by_method:
                strategies = [
                    strategy
                    for strategy in strategies
                    if strategy.provider_name
                    not in self.failed_providers_by_method[method]
                ]

            if strategies:
                logging.warning(
                    f"Pending balance of R$ {pending_amount:,.2f}. Trying fallback with providers of type {method}."
                )
                providers = [strategy.provider for strategy in strategies]
                processor = PaymentProcessor(providers)
                result = processor.process(pending_amount, method)
                if result:
                    logging.info(
                        f"Pending balance of R$ {pending_amount:,.2f} successfully processed by {result}."
                    )
                    return result
                else:
                    self.failed_providers_by_method.setdefault(method, []).extend(
                        [strategy.provider_name for strategy in strategies]
                    )
            else:
                logging.info(f"No provider available for method {method}.")
        return None
