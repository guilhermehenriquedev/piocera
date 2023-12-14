from _decimal import Decimal


def calcula_juros_asaas(valor_total):
    taxa_fixa = Decimal(0.49)
    juros_totais = Decimal((valor_total * Decimal(2.99)) / 100)
    valor_total = valor_total + juros_totais + taxa_fixa
    return valor_total
