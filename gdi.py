"""Gait Deviation Index (GDI), conforme calcula_GDI_LBA.m / calculate_GDI.m do laboratório.

Schwartz MH, Rozumalski A. The Gait Deviation Index: a new comprehensive index of gait
pathology. Gait Posture 2008;28:351-7.

- Base: 15 gait features do Gillette (dados_gdi/gillette.txt, 459 × 15).
- Controle: planilha GDI-GPS (dados_gdi/dados_con_GDI_orig.txt, 459 × 166 ciclos). É fixo e
  independente do grupo controle escolhido para as figuras.
- Cada ciclo vira um vetor de 459 valores: 9 variáveis × 51 pontos (0, 2, ..., 100% do ciclo),
  na ordem pelve sagital, coronal, transversal; quadril sagital, coronal, transversal; joelho
  sagital; tornozelo sagital; progressão do pé.
- d = distância entre os scores do ciclo (vetor × features) e a média dos scores dos controles.
- GDI = 100 − 10 × (log10 d − A) / B, com A e B = média e DP de log10 d dos controles.
"""
from pathlib import Path
import numpy as np
from indices import VARIAVEIS, _chave

PASTA = 'dados_gdi'
ARQ_FEATURES = 'gillette.txt'
ARQ_CONTROLES = 'dados_con_GDI_orig.txt'
N_PONTOS = 51


def vetores(curves, side):
    """Matriz 459 × n (um vetor por ciclo) a partir das curvas de 101 pontos (1:2:end do MATLAB)."""
    return np.vstack([curves[_chave(v, side)][::2] for v in VARIAVEIS])


def carregar_base(raiz):
    """Features, média dos scores dos controles e calibração A/B. None se os arquivos faltarem."""
    pasta = Path(raiz) / PASTA
    if not (pasta / ARQ_FEATURES).exists() or not (pasta / ARQ_CONTROLES).exists():
        return None
    features = np.loadtxt(pasta / ARQ_FEATURES)
    controles = np.loadtxt(pasta / ARQ_CONTROLES)
    if features.shape != (len(VARIAVEIS) * N_PONTOS, 15):
        raise ValueError(f'{ARQ_FEATURES}: esperado 459 × 15, encontrado {features.shape}.')
    if controles.shape[0] != len(VARIAVEIS) * N_PONTOS:
        raise ValueError(f'{ARQ_CONTROLES}: esperado 459 linhas, encontrado {controles.shape}.')
    scores = controles.T @ features
    media = scores.mean(axis=0)
    logd = np.log10(np.linalg.norm(scores - media, axis=1))
    return {'features': features, 'media_scores': media,
            'A': float(logd.mean()), 'B': float(logd.std(ddof=1)), 'n_controles': controles.shape[1]}


def gdi_vetores(vets, base):
    """GDI de cada coluna (ciclo) de uma matriz 459 × n."""
    d = np.linalg.norm(vets.T @ base['features'] - base['media_scores'], axis=1)
    return 100 - 10 * (np.log10(d) - base['A']) / base['B']


def calcular(curves, base):
    """GDI por ciclo e lado: {'D': array, 'E': array}."""
    return {side: gdi_vetores(vetores(curves, side), base) for side in ('D', 'E')}


def figura(resultados, nomes, titulo='Avaliação'):
    """Barras de GDI (média ± DP) por lado e condição; linha em 100 = média dos controles."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    from marcha import COR_LADO, COR_LADO_2
    cores = [COR_LADO, COR_LADO_2]
    fig, ax = plt.subplots(figsize=(5.2 + 1.3 * len(resultados), 4.6))
    fig.subplots_adjust(left=.13, right=.97, top=.86, bottom=.2)
    pos, rotulos, legenda = 0, [], []
    for i, r in enumerate(resultados):
        for s, lado in (('D', 'Direito'), ('E', 'Esquerdo')):
            m, dp = r[s].mean(), (r[s].std(ddof=1) if len(r[s]) > 1 else 0)
            ax.bar(pos, m, width=.7, color=cores[i][s], zorder=2)
            ax.errorbar(pos, m, yerr=dp, color='black', capsize=4, lw=1, zorder=3)
            ax.text(pos, m + dp + 1.5, f'{m:.1f}'.replace('.', ','), ha='center', fontsize=9, zorder=3)
            rotulos.append(lado)
            pos += 1
        pos += .6
    centros, p = [], 0
    for i in range(len(resultados)):
        centros += [p, p + 1]
        p += 2.6
    ax.set_xticks(centros, rotulos, fontsize=9)
    topo = max(110, max(r[s].mean() + r[s].std(ddof=1) for r in resultados for s in 'DE' if len(r[s]) > 1) + 8) \
        if any(len(r[s]) > 1 for r in resultados for s in 'DE') else 110
    ax.set_ylim(0, topo)
    ax.axhline(100, color='.35', lw=1, ls='--', zorder=1)
    ax.axhspan(90, 110, color='.9', zorder=0)
    ax.set_ylabel('GDI', fontsize=10)
    ax.spines[['top', 'right']].set_visible(False)
    if len(resultados) > 1:
        for i, c in enumerate(range(0, len(centros), 2)):
            ax.text((centros[c] + centros[c + 1]) / 2, -topo * .13, nomes[i], ha='center', fontsize=9.5, fontweight='bold')
    fig.suptitle(f'{titulo} — Gait Deviation Index (GDI)', fontsize=12.5)
    legenda = [Line2D([], [], color='.35', ls='--', label='Controle: 100'), Patch(color='.9', label='Controle ± 1 DP (90–110)')]
    fig.legend(handles=legenda, loc='upper center', bbox_to_anchor=(.55, .935), ncol=2, fontsize=8.5, frameon=False)
    return fig


def tabela(resultados, nomes):
    linhas = []
    for i, r in enumerate(resultados):
        for s, lado in (('D', 'Direito'), ('E', 'Esquerdo')):
            linhas.append({'Condição': nomes[i], 'Lado': lado, 'Variável': 'GDI', 'Média': round(float(r[s].mean()), 2),
                           'DP': round(float(r[s].std(ddof=1)), 2) if len(r[s]) > 1 else 0., 'Unidade': 'pontos', 'Ciclos': len(r[s])})
    return linhas


def resumo_comparacao(resultados, nomes):
    frases = []
    for s, lado in (('D', 'direito'), ('E', 'esquerdo')):
        a, b = resultados[0][s].mean(), resultados[1][s].mean()
        d = b - a
        f = lambda x: f'{x:.1f}'.replace('.', ',')
        frases.append(f'GDI {lado}: {f(a)} ({nomes[0]}) → {f(b)} ({nomes[1]}), diferença de '
                      f'{"+" if d >= 0 else "−"}{f(abs(d))} pontos.')
    return frases
