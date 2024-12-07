from typing import Dict, List, Optional
from strategy.payment.interfaces.provider_interface import Provider
from strategy.payment.services.payment_processor import PaymentProcessor
from strategy.payment.interfaces.payment_strategy import PaymentStrategy


class FallbackProcessor:
    def __init__(self, strategies_by_method: Dict[str, List[PaymentStrategy]]):
        self.strategies_by_method = strategies_by_method
        self.failed_providers_by_method = (
            {}
        )  # Rastreia provedores que já falharam por método de pagamento

    def process(self, pending_amount: float) -> Optional[str]:
        """
        Processa o saldo pendente com provedores de fallback para todos os métodos de pagamento.
        Retorna o nome do provedor que aprovou o pagamento ou None se todos falharem.
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
                print(
                    f"[WARNING] Saldo pendente de R$ {pending_amount:,.2f}. Tentando fallback com provedores do tipo {method}."
                )
                providers = [strategy.provider for strategy in strategies]
                processor = PaymentProcessor(providers)
                result = processor.process(pending_amount, method)
                if result:
                    print(
                        f"[SUCCESS] Saldo pendente de R$ {pending_amount:,.2f} processado com sucesso por {result}."
                    )
                    return result
                else:
                    self.failed_providers_by_method.setdefault(method, []).extend(
                        [strategy.provider_name for strategy in strategies]
                    )
            else:
                print(f"[INFO] Nenhum provedor disponível para o método {method}.")
        return None
