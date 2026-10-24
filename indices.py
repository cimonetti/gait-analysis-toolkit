"""Gait Profile Score (GPS), Gait Variable Score (GVS) e Movement Analysis Profile (MAP).

Baker R, et al. The Gait Profile Score and Movement Analysis Profile. Gait Posture 2009;30:265-9.
Diferença mínima clinicamente importante do GPS: 1,6° (Baker et al. Gait Posture 2012;35:612-5).

GVS de uma variável = RMS da diferença entre a curva do ciclo e a média do controle (101 pontos).
GPS de um lado = RMS dos 9 GVS daquele lado.
GPS geral = RMS de 15 GVS: 6 variáveis de cada lado + 3 da pelve (lado esquerdo, como em Baker).
"""
import csv
import io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

VARIAVEIS = ['Pelve_Sag', 'Pelve_Cor', 'Pelve_Trans', 'Quadril_Sag', 'Quadril_Cor',
             'Quadril_Trans', 'Joelho_Sag', 'Torn_Sag', 'Torn_Trans']
PELVE = VARIAVEIS[:3]
ROTULOS = {'Pelve_Sag': 'Pelve\nsagital', 'Pelve_Cor': 'Pelve\ncoronal', 'Pelve_Trans': 'Pelve\ntransversal',
           'Quadril_Sag': 'Quadril\nsagital', 'Quadril_Cor': 'Quadril\ncoronal', 'Quadril_Trans': 'Quadril\ntransversal',
           'Joelho_Sag': 'Joelho\nsagital', 'Torn_Sag': 'Tornozelo\nsagital', 'Torn_Trans': 'Progressão\ndo pé'}
DMCI = 1.6


def _chave(var, side):
    return var.replace('_', side + '_', 1)


def gvs_ciclos(curvas, media_controle):
    """GVS de cada ciclo (colunas) de uma variável."""
    return np.sqrt(np.mean((curvas - media_controle[:, None]) ** 2, axis=0))


def calcular(curves, medias):
    """GVS/GPS por lado e GPS geral. medias: {variável: curva média do controle}."""
    resultado = {}
    for side in ('D', 'E'):
        gvs = {v: gvs_ciclos(curves[_chave(v, side)], medias[v]) for v in VARIAVEIS}
        gps = np.sqrt(np.mean([gvs[v] ** 2 for v in VARIAVEIS], axis=0))
        resultado[side] = {'gvs': gvs, 'gps': gps, 'n': len(gps)}
    # Geral: média dos GVS² por variável (ciclos não pareados entre lados), pelve do lado esquerdo.
    quadrados = [np.mean(resultado[s]['gvs'][v] ** 2) for s in ('D', 'E') for v in VARIAVEIS if v not in PELVE]
    quadrados += [np.mean(resultado['E']['gvs'][v] ** 2) for v in PELVE]
    resultado['geral'] = float(np.sqrt(np.mean(quadrados)))
    return resultado


def referencia(carregados):
    """GPS e GVS dos próprios controles, deixando de fora a tentativa de cada ciclo.

    carregados: lista de dicionários de curvas (um por tentativa controle).
    Retorna médias do controle (todas as tentativas) e valores de referência.
    """
    medias, somas, total = {}, {}, 0
    for v in VARIAVEIS:
        todas = np.concatenate([t[_chave(v, s)] for t in carregados for s in ('D', 'E')], axis=1)
        medias[v] = todas.mean(axis=1)
        somas[v] = todas.sum(axis=1)
        total = todas.shape[1]
    gps, gvs = [], {v: [] for v in VARIAVEIS}
    for t in carregados:
        n_t = sum(t[_chave(VARIAVEIS[0], s)].shape[1] for s in ('D', 'E'))
        if total - n_t < 1:
            continue
        sem_t = {v: (somas[v] - sum(t[_chave(v, s)].sum(axis=1) for s in ('D', 'E'))) / (total - n_t)
                 for v in VARIAVEIS}
        for s in ('D', 'E'):
            if t[_chave(VARIAVEIS[0], s)].shape[1] == 0:
                continue
            g = {v: gvs_ciclos(t[_chave(v, s)], sem_t[v]) for v in VARIAVEIS}
            for v in VARIAVEIS:
                gvs[v].extend(g[v])
            gps.extend(np.sqrt(np.mean([g[v] ** 2 for v in VARIAVEIS], axis=0)))
    return {'medias': medias,
            'gps': (float(np.mean(gps)), float(np.std(gps, ddof=1))) if len(gps) > 1 else None,
            'gvs': {v: float(np.mean(gvs[v])) for v in VARIAVEIS} if gps else None,
            'n': len(gps)}


def _fmt(x):
    return f'{x:.1f}'.replace('.', ',')


def figura_map(resultados, nomes, ref=None, titulo='Avaliação'):
    """MAP: barras do GVS médio por variável e do GPS, por lado e condição."""
    from marcha import COR_LADO, COR_LADO_2
    cores = [COR_LADO, COR_LADO_2]
    grupos = VARIAVEIS + ['GPS']
    series = [(i, s) for i in range(len(resultados)) for s in ('D', 'E')]
    largura = .8 / len(series)
    fig, ax = plt.subplots(figsize=(11, 5.2))
    fig.subplots_adjust(left=.07, right=.99, top=.86, bottom=.19)
    x = np.arange(len(grupos))
    if ref and ref['gvs']:
        valores_ref = [ref['gvs'][v] for v in VARIAVEIS] + [ref['gps'][0]]
        ax.bar(x, valores_ref, width=.9, color='.88', zorder=0)
    for k, (i, s) in enumerate(series):
        r = resultados[i][s]
        valores = [r['gvs'][v].mean() for v in VARIAVEIS] + [r['gps'].mean()]
        pos = x - .4 + largura * (k + .5)
        ax.bar(pos, valores, width=largura * .92, color=cores[i][s], zorder=2)
        ax.text(pos[-1], valores[-1] + .3, _fmt(valores[-1]), ha='center', va='bottom', fontsize=7.5, zorder=3)
    ax.axvline(len(VARIAVEIS) - .5, color='.6', lw=.8, ls=':')
    ax.set_xticks(x, [ROTULOS.get(g, 'GPS') for g in grupos], fontsize=8.5)
    ax.set_ylabel('Graus (°)', fontsize=9)
    ax.set_xlim(-.6, len(grupos) - .4)
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(axis='y', labelsize=8.5)
    ax.yaxis.grid(True, color='.92', zorder=0)
    ax.set_axisbelow(True)
    geral = ' · '.join(f'GPS geral{" " + nomes[i] if len(resultados) > 1 else ""}: {_fmt(resultados[i]["geral"])}°'
                       for i in range(len(resultados)))
    fig.suptitle(f'{titulo} — Perfil de movimento (MAP)', fontsize=13)
    fig.text(.5, .905, geral, ha='center', fontsize=9.5)
    legenda = []
    for i in range(len(resultados)):
        sufixo = f' — {nomes[i]}' if len(resultados) > 1 else ''
        legenda += [Patch(color=cores[i]['D'], label='Direito' + sufixo), Patch(color=cores[i]['E'], label='Esquerdo' + sufixo)]
    if ref and ref['gvs']:
        legenda.append(Patch(color='.88', label='Controle (média)'))
    fig.legend(handles=legenda, loc='lower center', ncol=min(len(legenda), 5), fontsize=8.5, frameon=False)
    return fig


def tabela(resultados, nomes, ref=None):
    """Linhas para exibição/CSV: condição, lado, variável, média, DP, n."""
    linhas = []
    for i, r in enumerate(resultados):
        for s, lado in (('D', 'Direito'), ('E', 'Esquerdo')):
            for v in VARIAVEIS + ['GPS']:
                valores = r[s]['gps'] if v == 'GPS' else r[s]['gvs'][v]
                dp = float(np.std(valores, ddof=1)) if len(valores) > 1 else 0.
                linhas.append({'Condição': nomes[i], 'Lado': lado,
                               'Variável': 'GPS' if v == 'GPS' else ROTULOS[v].replace('\n', ' '),
                               'Média': round(float(np.mean(valores)), 2), 'DP': round(dp, 2),
                               'Unidade': '°', 'Ciclos': r[s]['n']})
        linhas.append({'Condição': nomes[i], 'Lado': 'Geral', 'Variável': 'GPS geral',
                       'Média': round(r['geral'], 2), 'DP': None, 'Unidade': '°', 'Ciclos': r['D']['n'] + r['E']['n']})
    if ref and ref['gps']:
        linhas.append({'Condição': 'Controle', 'Lado': 'Ambos', 'Variável': 'GPS (tentativa deixada de fora)',
                       'Média': round(ref['gps'][0], 2), 'DP': round(ref['gps'][1], 2), 'Unidade': '°', 'Ciclos': ref['n']})
    return linhas


def csv_texto(linhas):
    saida = io.StringIO()
    escritor = csv.DictWriter(saida, fieldnames=list(linhas[0]), delimiter=';')
    escritor.writeheader()
    for linha in linhas:
        escritor.writerow({k: ('' if v is None else str(v).replace('.', ',') if isinstance(v, float) else v)
                           for k, v in linha.items()})
    return '﻿' + saida.getvalue()


def resumo_comparacao(resultados, nomes):
    """Frases com a diferença de GPS entre as condições, frente à DMCI de 1,6°."""
    frases = []
    for rotulo, a, b in (('geral', resultados[0]['geral'], resultados[1]['geral']),
                         ('direito', resultados[0]['D']['gps'].mean(), resultados[1]['D']['gps'].mean()),
                         ('esquerdo', resultados[0]['E']['gps'].mean(), resultados[1]['E']['gps'].mean())):
        d = b - a
        criterio = 'acima' if abs(d) >= DMCI else 'abaixo'
        frases.append(f'GPS {rotulo}: {_fmt(a)}° ({nomes[0]}) → {_fmt(b)}° ({nomes[1]}), diferença de '
                      f'{"+" if d >= 0 else "−"}{_fmt(abs(d))}°, {criterio} da diferença mínima clinicamente importante (1,6°).')
    return frases
