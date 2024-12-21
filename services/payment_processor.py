from typing import List, Optional
from interfaces.provider_interface import Provider
import logging


class PaymentProcessor:
    def __init__(self, providers: List[Provider]):
        self.providers = providers

    def process(self, amount: float, method: str) -> Optional[str]:
        """
        Processes the payment with fallback among the available providers.
        Returns the name of the provider that approved the payment or None if all fail.
        """
        logging.info(
            f"Starting processing with fallback. Amount: R$ {amount:,.2f}, Method: {method}"
        )
        for provider in self.providers:
            if method in provider.supported_methods:
                logging.info(f"Trying to process with provider: {provider.name}...")
                try:
                    if provider.process_payment(method, amount):
                        logging.info(f"Payment approved by {provider.name}.")
                        return provider.name
                except Exception as e:
                    logging.error(f"Error processing with {provider.name}: {e}")
        logging.error("No provider was able to process the payment.")
        return None
