from strategy.payment.interfaces.payment_strategy import PaymentStrategy


class Checkout:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        """
        Define a estratégia de pagamento.
        """
        self._strategy = strategy

    def pay(self, amount: float):
        """
        Executa o pagamento usando a estratégia selecionada.
        """
        print(f"[INFO] Iniciando pagamento de R$ {amount:,.2f}.")
        self._strategy.pay(amount)
