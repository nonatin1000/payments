import logging
from typing import List
from interfaces.provider_interface import Provider
from providers.mercado_pago_provider import MercadoPagoProvider
from providers.pagarme_provider import PagarMeProvider
from providers.pagseguro_provider import PagSeguroProvider
from services.boleto_payment import BoletoPayment
from services.combined_payment import CombinedPayment
from services.credit_card_payment import CreditCardPayment
from services.pix_payment import PixPayment

logging.basicConfig(level=logging.INFO)


def main():
    try:
        # Configuração de provedores e estratégias
        logging.info("Configuring payment providers and strategies.")

        # Provedores reais
        pagseguro = PagSeguroProvider()
        mercado_pago = MercadoPagoProvider()
        pagarme = PagarMeProvider()

        # Payment strategies
        pix_pagseguro = PixPayment(pagseguro)
        pix_pagarme = PixPayment(pagarme)
        cartao_mercado_pago = CreditCardPayment(mercado_pago)
        cartao_pagarme = CreditCardPayment(pagarme)
        boleto_pagseguro = BoletoPayment(pagseguro)
        boleto_pagarme = BoletoPayment(pagarme)

        # Configuration of combined payments for each scenario
        combined_payments = []

        # Scenario 1: Successful PIX payment
        payment_pix_success = CombinedPayment()
        payment_pix_success.add_payment(pix_pagseguro, proportion=1.0)
        combined_payments.append(payment_pix_success)

        # Scenario 2: Credit Card fails with fallback to PagarMe
        payment_cc_fallback = CombinedPayment()
        payment_cc_fallback.add_payment(cartao_mercado_pago, proportion=1.0)
        payment_cc_fallback.add_payment(cartao_pagarme, proportion=0.0)
        combined_payments.append(payment_cc_fallback)

        # Scenario 3: Boleto fails with fallback to PagarMe
        payment_boleto_fallback = CombinedPayment()
        payment_boleto_fallback.add_payment(boleto_pagseguro, proportion=1.0)
        payment_boleto_fallback.add_payment(boleto_pagarme, proportion=0.0)
        combined_payments.append(payment_boleto_fallback)

        # Scenario 4: PIX fails with fallback to PagarMe
        payment_pix_fallback = CombinedPayment()
        payment_pix_fallback.add_payment(pix_pagseguro, proportion=1.0)
        payment_pix_fallback.add_payment(pix_pagarme, proportion=0.0)
        combined_payments.append(payment_pix_fallback)

        # Scenario 5: PIX and two credit cards, with one card failing
        payment_pix_two_cc = CombinedPayment()
        payment_pix_two_cc.add_payment(pix_pagseguro, proportion=0.5)
        payment_pix_two_cc.add_payment(cartao_mercado_pago, proportion=0.25)
        payment_pix_two_cc.add_payment(cartao_pagarme, proportion=0.25)
        combined_payments.append(payment_pix_two_cc)

        # Scenario 6: Combined PIX, boleto, and credit card
        payment_combined = CombinedPayment()
        payment_combined.add_payment(pix_pagseguro, proportion=0.4)
        payment_combined.add_payment(boleto_pagseguro, proportion=0.4)
        payment_combined.add_payment(cartao_pagarme, proportion=0.2)
        combined_payments.append(payment_combined)

        # Scenario 7: Multiple fallbacks for PIX
        payment_pix_multiple_fallback = CombinedPayment()
        payment_pix_multiple_fallback.add_payment(pix_pagseguro, proportion=0.5)
        payment_pix_multiple_fallback.add_payment(pix_pagarme, proportion=0.5)
        combined_payments.append(payment_pix_multiple_fallback)

        # Scenario 8: Multiple fallbacks for Credit Card
        payment_cc_multiple_fallback = CombinedPayment()
        payment_cc_multiple_fallback.add_payment(cartao_mercado_pago, proportion=0.5)
        payment_cc_multiple_fallback.add_payment(cartao_pagarme, proportion=0.5)
        combined_payments.append(payment_cc_multiple_fallback)

        # Scenario 9: Multiple fallbacks for Boleto
        payment_boleto_multiple_fallback = CombinedPayment()
        payment_boleto_multiple_fallback.add_payment(boleto_pagseguro, proportion=0.5)
        payment_boleto_multiple_fallback.add_payment(boleto_pagarme, proportion=0.5)
        combined_payments.append(payment_boleto_multiple_fallback)

        # Scenario 10: Mixed payment methods with fallbacks
        payment_mixed_fallback = CombinedPayment()
        payment_mixed_fallback.add_payment(pix_pagseguro, proportion=0.3)
        payment_mixed_fallback.add_payment(boleto_pagseguro, proportion=0.3)
        payment_mixed_fallback.add_payment(cartao_mercado_pago, proportion=0.4)
        combined_payments.append(payment_mixed_fallback)

        # Scenario 11: All methods with multiple fallbacks
        payment_all_methods_fallback = CombinedPayment()
        payment_all_methods_fallback.add_payment(pix_pagseguro, proportion=0.2)
        payment_all_methods_fallback.add_payment(pix_pagarme, proportion=0.2)
        payment_all_methods_fallback.add_payment(boleto_pagseguro, proportion=0.2)
        payment_all_methods_fallback.add_payment(boleto_pagarme, proportion=0.2)
        payment_all_methods_fallback.add_payment(cartao_mercado_pago, proportion=0.1)
        payment_all_methods_fallback.add_payment(cartao_pagarme, proportion=0.1)
        combined_payments.append(payment_all_methods_fallback)

        # Processing payments for each scenario
        total_amount = 300.00
        for idx, combined_payment in enumerate(combined_payments, start=1):
            logging.info("Processing scenario %d", idx)
            combined_payment.pay(total_amount=total_amount)

    except Exception as e:
        logging.error("An error occurred: %s", e)


if __name__ == "__main__":
    main()
