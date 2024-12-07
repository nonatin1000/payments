from typing import List, Optional
from strategy.payment.interfaces.provider_interface import Provider


class PaymentProcessor:
    def __init__(self, providers: List[Provider]):
        self.providers = providers

    def process(self, amount: float, method: str) -> Optional[str]:
        """
        Processa o pagamento com fallback entre os providers disponíveis.
        Retorna o nome do provider que aprovou o pagamento ou None se todos falharem.
        """
        print(
            f"[INFO] Iniciando processamento com fallback. Valor: R$ {amount:,.2f}, Método: {method}"
        )
        for provider in self.providers:
            if method in provider.supported_methods:
                print(f"[INFO] Tentando processar com o provedor: {provider.name}...")
                try:
                    if provider.process_payment(method, amount):
                        print(f"[SUCCESS] Pagamento aprovado por {provider.name}.")
                        return provider.name
                except Exception as e:
                    print(f"[ERROR] Erro ao processar com {provider.name}: {e}")
        print("[ERROR] Nenhum provedor conseguiu processar o pagamento.")
        return None
