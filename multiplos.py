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


def conferir_par(raw_qjt, raw_pp, nd, ne):
    """Confere se o PP pertence à mesma tentativa e tem a mesma divisão D/E do QJT."""
    def linhas(raw):
        try:
            text = raw.decode('utf-8-sig')
        except UnicodeDecodeError:
            text = raw.decode('cp1252')
        return [r.split('\t') for r in text.splitlines()[:2]]
    q, p = linhas(raw_qjt), linhas(raw_pp)
    if len(q) < 2 or len(p) < 2:
        return
    nome = lambda v: v.strip().replace('/', '\\').rsplit('\\', 1)[-1].casefold()
    origem_q = {nome(v) for v in q[0][1:] if v.strip()}
    origem_p = {nome(v) for v in p[0][1:] if v.strip()}
    if origem_q and origem_p and origem_q != origem_p:
        raise ValueError('QJT e PP vieram de arquivos C3D diferentes. Revise o par selecionado.')
    rotulos = [v.strip().upper() for v in p[1][1:]]
    pd, pe = rotulos.count('R_FOOT'), rotulos.count('L_FOOT')
    if pd + pe and (pd, pe) != (3*nd, 3*ne):
        raise ValueError(f'O PP tem {pd//3} ciclos direitos e {pe//3} esquerdos; o QJT tem {nd} e {ne}. Revise o par.')


def carregar_condicao(pares):
    """Lê e confere os pares de uma condição.

    pares: lista de (nome_qjt, bytes_qjt, nome_pp, bytes_pp, ciclos_d, ciclos_e).
    Retorna (curvas reunidas, procedência). Pontos ausentes ficam como NaN;
    os ciclos incompletos são tratados depois, na revisão.
    """
    import tempfile
    from pathlib import Path
    from marcha import read_txt
    from mapping import extract
    if not pares:
        raise ValueError('Selecione os arquivos QJT e PP.')
    if len({p[2] for p in pares}) != len(pares):
        raise ValueError('Um mesmo PP foi associado a mais de um QJT. Revise os pares.')
    if len({p[0] for p in pares}) != len(pares):
        raise ValueError('Há nomes QJT repetidos. Renomeie as tentativas para identificá-las sem ambiguidade.')
    loaded, provenance = [], []
    with tempfile.TemporaryDirectory() as folder:
        for i, (qn, qb, pn, pb, nd, ne) in enumerate(pares):
            if nd + ne == 0:
                raise ValueError(f'{qn}: informe pelo menos um ciclo.')
            inferred = ciclos_cabecalho(qb)
            if inferred is not None and inferred != (nd, ne):
                raise ValueError(f'{qn}: quantidades informadas divergem do cabeçalho {inferred}.')
            conferir_par(qb, pb, nd, ne)
            qp = Path(folder) / f'qjt_{i}.txt'; pp = Path(folder) / f'pp_{i}.txt'
            qp.write_bytes(qb); pp.write_bytes(pb)
            try:
                qdata, pdata = read_txt(qp, permitir_ausentes=True), read_txt(pp, permitir_ausentes=True)
            except ValueError as exc:
                raise ValueError(str(exc).replace(qp.name, qn).replace(pp.name, pn)) from exc
            if qdata.shape[1] != 1 + 9*(nd+ne) or pdata.shape[1] != 1 + 6*(nd+ne):
                raise ValueError(f'{qn} / {pn}: colunas incompatíveis com os ciclos informados.')
            loaded.append(extract(qdata, pdata, nd, ne))
            provenance.append({'qjt': qn, 'pp': pn, 'ciclos_d': nd, 'ciclos_e': ne})
    return reunir_ciclos(loaded), provenance
