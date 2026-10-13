"""Pareamento e reunião de ciclos de diferentes tentativas."""
import re
import numpy as np


def chave_par(nome):
    """Identifica a mesma tentativa pelos nomes QJT/PP ou Quadril/Pelve."""
    return re.sub(r'(^|_)(qjt|pp|quadril|pelve)(?=_|\.|$)', r'\1segmento', nome.casefold())


def ciclos_cabecalho(raw):
    """Retorna D/E quando o cabeçalho QJT tem os seis blocos esperados."""
    try:
        text = raw.decode('utf-8-sig')
    except UnicodeDecodeError:
        text = raw.decode('cp1252')
    rows = text.splitlines()
    if len(rows) < 5:
        return None
    labels = [v.strip().upper() for v in rows[1].split('\t')[1:]]
    nd, ne = labels.count('QUADRIL_D'), labels.count('QUADRIL_E')
    if nd % 3 or ne % 3 or nd + ne == 0:
        return None
    expected = [('QUADRIL_D',nd),('QUADRIL_E',ne),('JOELHO_D',nd),
                ('JOELHO_E',ne),('R_FOOT',nd),('L_FOOT',ne)]
    flattened = [label for label, count in expected for _ in range(count)]
    if labels != flattened:
        return None
    return nd // 3, ne // 3


def reunir_ciclos(tentativas):
    """Concatena colunas (ciclos), mantendo os 101 pontos de cada curva."""
    if not tentativas:
        raise ValueError('Adicione pelo menos um par de arquivos.')
    keys = set(tentativas[0])
    if any(set(t) != keys for t in tentativas):
        raise ValueError('Tentativas com curvas incompatíveis.')
    for t in tentativas:
        if any(v.ndim != 2 or v.shape[0] != 101 for v in t.values()):
            raise ValueError('Cada curva deve ter 101 pontos e uma coluna por ciclo.')
    result = {key: np.concatenate([t[key] for t in tentativas], axis=1)
              for key in tentativas[0]}
    if any(values.shape[1] == 0 for values in result.values()):
        raise ValueError('O conjunto precisa conter pelo menos um ciclo de cada lado.')
    return result
