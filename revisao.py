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


def ciclos_incompletos(curves, identities):
    """IDs dos ciclos com algum ponto ausente em qualquer segmento."""
    result=[]
    for side,rows in identities.items():
        for r in rows:
            if any(np.isnan(values[:,r['coluna']]).any()
                   for key,values in curves.items() if ('D_' if side=='D' else 'E_') in key):
                result.append(r['id'])
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
    incompletos=sorted(set(ciclos_incompletos(curves,identities))-excluded)
    if incompletos:
        raise ValueError('Ciclos com pontos ausentes não podem entrar nas figuras: '+', '.join(incompletos)+
                         '. Mantenha-os na lista de excluídos.')
    return result
