import sys
import os
from typing import List
from strategy.payment.interfaces.provider_interface import Provider
from strategy.payment.services.boleto_payment import BoletoPayment
from strategy.payment.services.combined_payment import CombinedPayment
from strategy.payment.services.credit_card_payment import CreditCardPayment
from strategy.payment.services.pix_payment import PixPayment


class FakeProvider(Provider):
    def __init__(
        self, name: str, supported_methods: List[str], should_fail: bool = False
    ):
        self._name = name
        self._supported_methods = supported_methods
        self.should_fail = should_fail

    @property
    def name(self) -> str:
        return self._name

    @property
    def supported_methods(self) -> List[str]:
        return self._supported_methods

    def process_payment(self, payment_method: str, amount: float) -> bool:
        if self.should_fail:
            raise Exception(f"Método {payment_method} não suportado por {self.name}")
        print(
            f"[{self.name}] Processando pagamento de R$ {amount:.2f} via {payment_method}."
        )
        return True


def main():
    try:
        # Configuração de provedores e estratégias
        print("[INFO] Configurando provedores e estratégias de pagamento.")

        # Provedores para simulação
        pagseguro = FakeProvider(
            name="PagSeguro", supported_methods=["pix", "boleto", "credit_card"]
        )
        mercado_pago_fail = FakeProvider(
            name="MercadoPago", supported_methods=["credit_card"], should_fail=True
        )
        pagarme_success = FakeProvider(
            name="PagarMe", supported_methods=["credit_card"]
        )
        pagarme_fail = FakeProvider(
            name="PagarMe", supported_methods=["boleto"], should_fail=True
        )
        pagarme_pix_success = FakeProvider(name="PagarMe", supported_methods=["pix"])
        pagseguro_boleto_fail = FakeProvider(
            name="PagSeguro", supported_methods=["boleto"], should_fail=True
        )
        pagarme_credit_fail = FakeProvider(
            name="PagarMe", supported_methods=["credit_card"], should_fail=True
        )
        pagarme_credit_success = FakeProvider(
            name="PagarMe", supported_methods=["credit_card"]
        )

        # Estratégias de pagamento
        pix_pagseguro = PixPayment(pagseguro)
        pix_pagarme = PixPayment(pagarme_pix_success)
        cartao_mercado_pago = CreditCardPayment(mercado_pago_fail)
        cartao_pagarme_success = CreditCardPayment(pagarme_success)
        cartao_pagarme_fail = CreditCardPayment(pagarme_credit_fail)
        boleto_pagseguro = BoletoPayment(pagseguro_boleto_fail)
        boleto_pagarme = BoletoPayment(pagarme_success)

        # Configuração de pagamentos combinados para cada cenário
        combined_payments = []

        # Cenário 1: PIX sucesso
        payment_pix_success = CombinedPayment()
        payment_pix_success.add_payment(pix_pagseguro, proportion=1.0)
        combined_payments.append(payment_pix_success)

        # Cenário 2: Credit Card falha com fallback para PagarMe
        payment_cc_fallback = CombinedPayment()
        payment_cc_fallback.add_payment(cartao_mercado_pago, proportion=1.0)
        payment_cc_fallback.add_payment(cartao_pagarme_success, proportion=0.0)
        combined_payments.append(payment_cc_fallback)

        # Cenário 3: Boleto falha com fallback para PagarMe
        payment_boleto_fallback = CombinedPayment()
        payment_boleto_fallback.add_payment(boleto_pagseguro, proportion=1.0)
        payment_boleto_fallback.add_payment(boleto_pagarme, proportion=0.0)
        combined_payments.append(payment_boleto_fallback)

        # Cenário 4: PIX falha com fallback para PagarMe
        payment_pix_fallback = CombinedPayment()
        payment_pix_fallback.add_payment(pix_pagseguro, proportion=1.0)
        payment_pix_fallback.add_payment(pix_pagarme, proportion=0.0)
        combined_payments.append(payment_pix_fallback)

        # Cenário 5: PIX e dois cartões de crédito, com um cartão falhando
        payment_pix_two_cc = CombinedPayment()
        payment_pix_two_cc.add_payment(pix_pagseguro, proportion=0.5)
        payment_pix_two_cc.add_payment(cartao_mercado_pago, proportion=0.25)
        payment_pix_two_cc.add_payment(cartao_pagarme_success, proportion=0.25)
        combined_payments.append(payment_pix_two_cc)

        # Cenário 6: Combinado pix, boleto e crédito
        payment_combined = CombinedPayment()
        payment_combined.add_payment(pix_pagseguro, proportion=0.4)
        payment_combined.add_payment(boleto_pagseguro, proportion=0.4)
        payment_combined.add_payment(cartao_pagarme_fail, proportion=0.2)
        combined_payments.append(payment_combined)

        # Processamento dos pagamentos para cada cenário
        total_amount = 300.00
        for idx, combined_payment in enumerate(combined_payments, start=1):
            print(f"\n[INFO] Processando cenário {idx}")
            combined_payment.pay(total_amount=total_amount)

    except Exception as e:
        print(f"[ERROR] Um erro ocorreu: {e}")


if __name__ == "__main__":
    main()
