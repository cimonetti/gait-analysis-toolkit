"""Identidade e remoção consistente de ciclos em todos os segmentos."""
import numpy as np


def identificar_ciclos(provenance):
    result={'D':[], 'E':[]}
    for attempt,r in enumerate(provenance,1):
        for side in result:
            for local in range(r['ciclos_'+side.lower()]):
                index=len(result[side])
                result[side].append({'id':f'{side}{index+1}', 'lado':side,
                    'coluna':index, 'tentativa':attempt, 'ciclo_local':local+1,
                    'qjt':r['qjt'], 'pp':r['pp']})
    return result


def remover_ciclos(curves, identities, excluded):
    excluded=set(excluded)
    known={r['id'] for rows in identities.values() for r in rows}
    if excluded-known:
        raise ValueError('Ciclo desconhecido na lista de exclusões.')
    masks={side:np.array([r['id'] not in excluded for r in rows],dtype=bool)
           for side,rows in identities.items()}
    if any(not mask.any() for mask in masks.values()):
        raise ValueError('Mantenha pelo menos um ciclo de cada lado para exportar as duas figuras.')
    result={}
    for key,values in curves.items():
        side='D' if 'D_' in key else 'E'
        if values.shape[1] != len(masks[side]):
            raise ValueError('Identificação dos ciclos incompatível com os dados.')
        result[key]=values[:,masks[side]].copy()
    return result
