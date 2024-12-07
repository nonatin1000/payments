from strategy.payment.interfaces.payment_strategy import PaymentStrategy
from strategy.payment.services.fallback_processor import FallbackProcessor


class CombinedPayment(PaymentStrategy):
    def __init__(self):
        self.payments = []

    def add_payment(self, payment_strategy: PaymentStrategy, proportion: float):
        """
        Adiciona uma estratégia de pagamento.

        :param payment_strategy: Instância de PaymentStrategy.
        :param proportion: Proporção do valor total para este pagamento.
        """
        if proportion < 0 or proportion > 1:
            raise ValueError("Proporção deve estar entre 0 e 1.")
        self.payments.append({"strategy": payment_strategy, "proportion": proportion})

    def pay(self, total_amount: float):
        """
        Processa o pagamento usando as estratégias combinadas.

        :param total_amount: Valor total a ser pago.
        """
        if not self.payments:
            raise ValueError("Nenhuma estratégia de pagamento foi adicionada.")

        print(f"[INFO] Pagamento combinado de R$ {total_amount:,.2f} iniciado.")
        pending_amount = total_amount

        # Agrupa as estratégias por tipo de pagamento
        strategies_by_method = self._group_strategies_by_method()
        fallback_processor = FallbackProcessor(strategies_by_method)

        # Processa cada tipo de pagamento independentemente
        for payment in self.payments:
            if pending_amount <= 0:
                break

            pending_amount = self._process_payment(
                payment, total_amount, pending_amount
            )

        # Processa saldo pendente com fallback por todos os métodos de pagamento
        if pending_amount > 0:
            result = fallback_processor.process(pending_amount)
            if result:
                pending_amount = 0

        # Verifica se o pagamento foi completado
        if pending_amount > 0:
            self._handle_payment_failure(total_amount - pending_amount, total_amount)
        else:
            print(
                f"[INFO] Pagamento concluído com sucesso. Total pago: R$ {total_amount:,.2f}."
            )

    def _process_payment(self, payment, total_amount, pending_amount):
        """
        Processa uma tentativa de pagamento.

        :param payment: Estratégia de pagamento configurada.
        :param total_amount: Valor total a ser pago.
        :param pending_amount: Valor ainda pendente.
        :return: Valor pendente após a tentativa de pagamento.
        """
        strategy = payment["strategy"]
        proportion = payment["proportion"]
        amount_to_pay = total_amount * proportion

        if amount_to_pay == 0:
            return pending_amount

        try:
            print(
                f"[INFO] Tentando pagar R$ {amount_to_pay:,.2f} com {strategy.provider_name}."
            )
            strategy.pay(amount_to_pay)
            print(f"[SUCCESS] R$ {amount_to_pay:,.2f} processados com sucesso.")
            return pending_amount - amount_to_pay
        except Exception as e:
            print(
                f"[ERROR] Falha ao processar R$ {amount_to_pay:,.2f} com {strategy.provider_name}: {e}"
            )
            return pending_amount

    def _handle_payment_failure(self, total_paid, total_amount):
        """
        Lida com falhas ao concluir o pagamento.

        :param total_paid: Valor já processado.
        :param total_amount: Valor total esperado.
        """
        print(
            f"[ERROR] Não foi possível concluir o pagamento de R$ {total_amount:,.2f}."
        )
        print(
            f"[CANCEL] Revertendo transações realizadas. Total a ser estornado: R$ {total_paid:,.2f}."
        )

    def _group_strategies_by_method(self):
        """
        Agrupa estratégias por tipo de pagamento.

        :return: Dicionário com tipos de pagamento como chave e estratégias como valor.
        """
        grouped = {}
        for payment in self.payments:
            strategy = payment["strategy"]
            method = strategy.payment_method
            if method not in grouped:
                grouped[method] = []
            grouped[method].append(strategy)
        return grouped

    @property
    def payment_method(self) -> str:
        return "COMBINED"

    @property
    def provider_name(self) -> str:
        return "MULTIPLE"
