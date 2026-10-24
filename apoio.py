"""Saída do pé (% do ciclo) a partir dos tempos de apoio, balanço e ciclo."""


def saida_do_pe(apoio, dp_apoio, ciclo, balanco=None, dp_balanco=None):
    """Média = apoio ÷ ciclo; DP = DP do apoio ÷ ciclo (ambos em % do ciclo).

    Balanço é usado só para conferência (apoio + balanço ≈ ciclo) e para
    informar a fase de balanço em % do ciclo.
    """
    if not ciclo or ciclo <= 0:
        raise ValueError('Informe a duração do ciclo.')
    if not apoio or apoio <= 0:
        raise ValueError('Informe o tempo de apoio.')
    if apoio >= ciclo:
        raise ValueError('O tempo de apoio deve ser menor que a duração do ciclo.')
    if dp_apoio is None or dp_apoio < 0:
        raise ValueError('O DP do apoio não pode ser negativo.')
    resultado = {'media': 100*apoio/ciclo, 'dp': 100*dp_apoio/ciclo, 'aviso': None, 'balanco': None}
    if balanco:
        resultado['balanco'] = (100*balanco/ciclo, 100*(dp_balanco or 0)/ciclo)
        soma = apoio + balanco
        if abs(soma - ciclo) > .05*ciclo:
            resultado['aviso'] = (f'Apoio + balanço = {soma:.3f} s, diferente do ciclo ({ciclo:.3f} s) em mais de 5%. '
                                  'Confira os valores.')
    return resultado
