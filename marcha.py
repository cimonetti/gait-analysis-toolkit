"""Processamento de marcha e figuras para laudos, sem dependência do MATLAB."""
from pathlib import Path
import argparse
import json
import warnings
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from mapping import extract

ROOT = Path(__file__).resolve().parent

def read_txt(path):
    path = Path(path)
    if not path.exists() and not path.suffix:
        path = path.with_suffix('.txt')
    if not path.exists():
        raise FileNotFoundError(f'Arquivo não encontrado: {path}')
    raw = path.read_bytes()
    try:
        text = raw.decode('utf-8-sig')
    except UnicodeDecodeError:
        text = raw.decode('cp1252')
    rows = []
    for lineno, line in enumerate(text.splitlines()[5:], 6):
        if not line.strip():
            continue
        tokens = line.split('\t')
        if tokens[-1] == '':
            tokens.pop()
        try:
            rows.append([float(t) if t.strip() else np.nan for t in tokens])
        except ValueError as exc:
            raise ValueError(f'{path.name}, linha {lineno}: conteúdo não numérico.') from exc
    if not rows or len({len(r) for r in rows}) != 1:
        raise ValueError(f'{path.name}: linhas vazias ou quantidade irregular de colunas.')
    data = np.asarray(rows)
    if data.shape[0] != 101:
        raise ValueError(f'{path.name}: esperado ciclo normalizado de 101 pontos, recebido {data.shape[0]}.')
    if not np.isfinite(data).all():
        raise ValueError(f'{path.name}: contém valores ausentes ou não finitos. Revise a exportação.')
    return data

def load_record(record, base, allow_unilateral=False):
    nd, ne = record['ciclos_d'], record['ciclos_e']
    if any(isinstance(n, bool) or not isinstance(n, int) or n < (0 if allow_unilateral else 1) for n in (nd, ne)):
        raise ValueError('Informe pelo menos um ciclo inteiro de cada lado.')
    if nd + ne == 0:
        raise ValueError('Nenhum ciclo disponível.')
    return extract(read_txt(base / record['qjt']), read_txt(base / record['pp']), nd, ne)

def statistics(curves):
    return curves.mean(axis=1), curves.std(axis=1, ddof=1) if curves.shape[1] > 1 else np.zeros(101)

def reference(records, base, dp_mode='ambos'):
    if not records:
        return None
    loaded = [load_record(r, base, allow_unilateral=True) for r in records]
    ref = {}
    for key in json.loads((ROOT / 'plots.json').read_text(encoding='utf-8')):
        both = np.concatenate([r[key.replace('_', 'D_', 1)] for r in loaded] +
                              [r[key.replace('_', 'E_', 1)] for r in loaded], axis=1)
        mean, sd = statistics(both)
        if key == 'Pelve_Sag' and dp_mode == 'esquerdo':
            _, sd = statistics(np.concatenate([r['PelveE_Sag'] for r in loaded], axis=1))
        elif dp_mode not in ('esquerdo', 'ambos'):
            raise ValueError('controle_dp_pelve_sag deve ser esquerdo ou ambos.')
        ref[key] = (mean, sd)
    return ref

def make_figure(curves, side, plots, ref=None, stance=None, title='Avaliação', individual=True):
    fig, axes = plt.subplots(4, 3, figsize=(9, 11))
    fig.subplots_adjust(left=.13, right=.98, bottom=.07, top=.91, hspace=.65, wspace=.55)
    fig.suptitle(f'{title} — {"Direito" if side == "D" else "Esquerdo"}', fontsize=14)
    axes.flat[9].set_visible(False)
    x = np.arange(101)
    for key, spec in plots.items():
        ax = axes.flat[spec['slot']]
        if ref:
            mean, sd = ref[key]
            ax.fill_between(x, mean-sd, mean+sd, color='.82', alpha=.8)
            ax.plot(x, mean, color='.45', lw=1)
        if stance is not None:
            mean, sd = stance
            if not 0 <= mean <= 100 or sd < 0:
                raise ValueError('Apoio: média entre 0 e 100 e DP não negativo.')
            ax.axvspan(mean-sd, mean+sd, color='.9', alpha=.65)
            ax.axvline(mean, color='black', lw=.8)
        if curves is not None:
            values = curves[key.replace('_', side+'_', 1)]
            color = '#1565c0' if side == 'D' else '#c62828'
            ax.plot(x, values if individual else values.mean(axis=1), color=color, lw=1)
        limits = spec['ylim']
        if limits is not None:
            if len(limits) != 2 or limits[0] >= limits[1]:
                raise ValueError(f'Limites Y inválidos: {key}')
            ax.set_ylim(*limits)
            if curves is not None and (values.min() < limits[0] or values.max() > limits[1]):
                warnings.warn(f'{key} ({side}): curvas ultrapassam os limites Y definidos.')
        if spec.get('yticks') is not None:
            ax.set_yticks(spec['yticks'])
        ax.set_xlim(0, 100)
        ax.axhline(0, color='black', lw=.6)
        ax.set_title(spec['title'], fontsize=10)
        ax.set_xlabel('Ciclo (%)', fontsize=8)
        ax.set_ylabel('Graus (°)', fontsize=8)
        ax.tick_params(labelsize=8)
        for y, label in zip((.12, .88), spec['labels']):
            ax.text(-.29, y, label, transform=ax.transAxes, rotation=90,
                    ha='center', va='center', fontsize=7)
    legend=[]
    if curves is not None:
        legend.append(Line2D([0],[0],color='#1565c0' if side=='D' else '#c62828',label='Ciclos da avaliação' if individual else 'Média da avaliação'))
    if ref:
        legend.append(Line2D([0],[0],color='.7',lw=7,label='Controle: média ± 1 DP'))
    fig.legend(handles=legend,loc='lower center',ncol=2,fontsize=9)
    return fig

def make_comparison(curves, plots, ref=None, title='Avaliação'):
    """Médias dos ciclos mantidos por lado e referência nas mesmas escalas."""
    fig=make_figure(None,'D',plots,ref,None,title)
    fig.suptitle(f'{title} — Comparação das médias',fontsize=14)
    x=np.arange(101)
    for key,spec in plots.items():
        ax=fig.axes[spec['slot']]
        for side,color in [('D','#1565c0'),('E','#c62828')]:
            mean=curves[key.replace('_',side+'_',1)].mean(axis=1)
            ax.plot(x,mean,color=color,lw=1.8)
    for legend in list(fig.legends): legend.remove()
    handles=[Line2D([0],[0],color='#1565c0',lw=2,label='Média direita'),
             Line2D([0],[0],color='#c62828',lw=2,label='Média esquerda')]
    if ref: handles.append(Line2D([0],[0],color='.45',lw=2,label='Controle: média ± 1 DP'))
    fig.legend(handles=handles,loc='lower center',ncol=3,fontsize=9)
    return fig

def run(config_path=ROOT/'config.json', controls_only=False, show=False):
    path = Path(config_path).resolve()
    config = json.loads(path.read_text(encoding='utf-8'))
    plots_path = path.parent / config.get('config_graficos', 'plots.json')
    plots = json.loads(plots_path.read_text(encoding='utf-8'))
    base = path.parent
    ref = reference(config.get('controles', []), base, config.get('controle_dp_pelve_sag', 'ambos'))
    if controls_only and ref is None:
        raise ValueError('Cadastre ao menos um controle.')
    record = config['avaliacao']
    curves = None if controls_only else load_record(record, base)
    out = base/config.get('saida','figuras')
    out.mkdir(parents=True, exist_ok=True)
    generated=[]
    for side in ('D','E'):
        fig = make_figure(curves, side, plots, ref,
                          None if controls_only else record.get('apoio_'+side.lower()),
                          'Controle' if controls_only else record.get('titulo','Avaliação'),
                          config.get('ciclos_individuais',True))
        stem = ('controle' if controls_only else 'avaliacao')+'_'+side
        for ext in ('png','svg'):
            target=out/f'{stem}.{ext}'
            fig.savefig(target,dpi=300)
            generated.append(target)
        plt.close(fig)
    if curves is not None:
        fig=make_comparison(curves,plots,ref,record.get('titulo','Avaliação'))
        for ext in ('png','svg'):
            target=out/f'comparacao_medias.{ext}'
            fig.savefig(target,dpi=300)
            generated.append(target)
        plt.close(fig)
    if ref:
        np.savez(out/'controle.npz',**{k+'_'+s:v[i] for k,v in ref.items() for i,s in enumerate(('media','dp'))})
    if curves:
        np.savez(out/'avaliacao_ciclos.npz',**curves)
    return generated

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',default=str(ROOT/'config.json'))
    parser.add_argument('--controle',action='store_true')
    args=parser.parse_args()
    try:
        for file in run(args.config,args.controle):
            print(file)
    except (ValueError, FileNotFoundError, KeyError) as exc:
        parser.exit(1, f'Erro: {exc}\n')
