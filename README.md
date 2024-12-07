# Gestão de Múltiplos Provedores de Pagamento

## Descrição do Projeto

O projeto "Gestão de Múltiplos Provedores de Pagamento" visa criar um sistema robusto e flexível para gerenciar transações financeiras utilizando diversos provedores de pagamento. Utilizando o padrão de projeto Strategy, o sistema permite combinar diferentes métodos de pagamento, tais como Pix, cartão de crédito, boleto, e suas combinações, proporcionando uma solução escalável e adaptável para as necessidades de processamento de pagamentos de qualquer organização.

## Funcionalidades Principais

1. **Suporte a Múltiplos Provedores**:
   - Integração com diferentes provedores de pagamento, como PagSeguro, MercadoPago, PagarMe, entre outros.
   - Possibilidade de adicionar novos provedores de forma simplificada e modular.

2. **Diversos Métodos de Pagamento**:
   - Suporte a transações via Pix, cartão de crédito e boleto bancário.
   - Combinação flexível de métodos de pagamento, permitindo transações combinadas (Pix + Cartão de Crédito, dois cartões, Pix + Boleto, etc.).

3. **Fallback e Tolerância a Falhas**:
   - Implementação de mecanismos de fallback para garantir a continuidade das transações em caso de falha de um provedor específico.
   - Priorização e tentativa de múltiplos provedores até que o pagamento seja processado com sucesso.

4. **Estratégias de Pagamento Combinado**:
   - Possibilidade de dividir uma única transação entre diferentes métodos e provedores, conforme necessidades específicas.
   - Proporções configuráveis para distribuir o valor da transação entre os métodos de pagamento selecionados.

## Benefícios

- **Escalabilidade**: Fácil adição de novos provedores e métodos de pagamento sem necessidade de grandes mudanças no sistema.
- **Flexibilidade**: Capacidade de combinar e configurar diferentes métodos de pagamento para atender a diversas estratégias comerciais.
- **Resiliência**: Mecanismos de fallback asseguram que as transações sejam concluídas mesmo em caso de falha de um provedor.
- **Modularidade**: Arquitetura modular baseada no padrão Strategy facilita a manutenção e evolução do sistema.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal para o desenvolvimento do sistema.
- **Padrão de Projeto Strategy**: Utilizado para implementar as estratégias de pagamento e gestão de provedores.
- **Integração com APIs de Provedores de Pagamento**: Comunicação com diferentes serviços de pagamento para realizar transações.

## Exemplos de Cenários de Pagamento

### Cenário 1: Sucesso com PIX

```python
# Configuração de pagamento apenas com PIX
pix_pagseguro = PixPayment(pagseguro)
combined_payment = CombinedPayment()
combined_payment.add_payment(pix_pagseguro, proportion=1.0)
combined_payment.pay(total_amount=300.00)

# Configuração de pagamento com fallback de cartão de crédito
cartao_mercado_pago = CreditCardPayment(mercado_pago_fail)
cartao_pagarme = CreditCardPayment(pagarme_success)
combined_payment = CombinedPayment()
combined_payment.add_payment(cartao_mercado_pago, proportion=1.0)
combined_payment.add_payment(cartao_pagarme, proportion=0.0)
combined_payment.pay(total_amount=300.00)

# Configuração de pagamento com fallback de boleto
boleto_pagseguro = BoletoPayment(pagseguro_boleto_fail)
boleto_pagarme = BoletoPayment(pagarme_success)
combined_payment = CombinedPayment()
combined_payment.add_payment(boleto_pagseguro, proportion=1.0)
combined_payment.add_payment(boleto_pagarme, proportion=0.0)
combined_payment.pay(total_amount=300.00)

# Configuração de pagamento com fallback de PIX
pix_pagseguro = PixPayment(pagseguro)
pix_pagarme = PixPayment(pagarme_pix_success)
combined_payment = CombinedPayment()
combined_payment.add_payment(pix_pagseguro, proportion=1.0)
combined_payment.add_payment(pix_pagarme, proportion=0.0)
combined_payment.pay(total_amount=300.00)

# Configuração de pagamento com PIX e dois cartões de crédito
pix_pagseguro = PixPayment(pagseguro)
cartao_mercado_pago = CreditCardPayment(mercado_pago_fail)
cartao_pagarme = CreditCardPayment(pagarme_success)
combined_payment = CombinedPayment()
combined_payment.add_payment(pix_pagseguro, proportion=0.5)
combined_payment.add_payment(cartao_mercado_pago, proportion=0.25)
combined_payment.add_payment(cartao_pagarme, proportion=0.25)
combined_payment.pay(total_amount=300.00)

# Configuração de pagamento combinado com PIX, boleto e crédito
pix_pagseguro = PixPayment(pagseguro)
boleto_pagseguro = BoletoPayment(pagseguro_boleto_fail)
cartao_pagarme = CreditCardPayment(pagarme_credit_fail)
combined_payment = CombinedPayment()
combined_payment.add_payment(pix_pagseguro, proportion=0.4)
combined_payment.add_payment(boleto_pagseguro, proportion=0.4)
combined_payment.add_payment(cartao_pagarme, proportion=0.2)
combined_payment.pay(total_amount=300.00)
