"""Mapeamento literal de processaMarcha.m (índices MATLAB começam em 1)."""
import numpy as np

def extract(qjt, pp, nd, ne):
    def take(data, first, last, sign, expected):
        if expected == 0:
            return np.empty((data.shape[0], 0))
        columns = np.arange(first-1, last, 3, dtype=int)
        if len(columns) != expected or columns[-1] >= data.shape[1]:
            raise ValueError("Número de ciclos incompatível com as colunas do TXT.")
        return data[:, columns] * sign
    curves = {}
    curves['PelveD_Sag'] = take(pp, 3, nd*3+1, 1, nd)
    curves['PelveD_Cor'] = take(pp, 2, nd*3+1, -1, nd)
    curves['PelveD_Trans'] = take(pp, 4, nd*3+1, 1, nd)
    curves['QuadrilD_Sag'] = take(qjt, 2, nd*3+1, 1, nd)
    curves['QuadrilD_Cor'] = take(qjt, 3, nd*3+1, 1, nd)
    curves['QuadrilD_Trans'] = take(qjt, 4, nd*3+1, 1, nd)
    curves['JoelhoD_Sag'] = take(qjt, ((nd+1)*3-1)+3*ne, (((nd+1)*3-1)+3*ne)+3*nd-1, 1, nd)
    curves['JoelhoD_Cor'] = take(qjt, ((nd+1)*3-1)+3*ne+1, (((nd+1)*3-1)+3*ne)+3*nd-1, 1, nd)
    curves['JoelhoD_trans'] = take(qjt, ((nd+1)*3-1)+3*ne+2, (((nd+1)*3-1)+3*ne)+3*nd-1, 1, nd)
    curves['TornD_Sag'] = take(qjt, ((((nd+1)*3-1)+3*ne)+3*nd)+3*ne, (((((nd+1)*3-1)+3*ne)+3*nd)+3*ne-1)+3*nd, 1, nd)
    curves['TornD_Trans'] = take(pp, (nd*3+2)+3*ne+2, ((nd*3+2)+3*ne-1)+3*nd, 1, nd)
    curves['PelveE_Sag'] = take(pp, nd*3+3, (nd*3+2)+3*ne-1, 1, ne)
    curves['PelveE_Cor'] = take(pp, nd*3+2, (nd*3+2)+3*ne-1, 1, ne)
    curves['PelveE_Trans'] = take(pp, nd*3+4, (nd*3+2)+3*ne-1, -1, ne)
    curves['QuadrilE_Sag'] = take(qjt, (nd+1)*3-1, ((nd+1)*3-1)+3*ne-1, 1, ne)
    curves['QuadrilE_Cor'] = take(qjt, (nd+1)*3, ((nd+1)*3-1)+3*ne-1, 1, ne)
    curves['QuadrilE_Trans'] = take(qjt, (nd+1)*3+1, ((nd+1)*3-1)+3*ne-1, 1, ne)
    curves['JoelhoE_Sag'] = take(qjt, (((nd+1)*3-1)+3*ne)+3*nd, ((((nd+1)*3-1)+3*ne)+3*nd)+3*ne-1, 1, ne)
    curves['JoelhoE_Cor'] = take(qjt, (((nd+1)*3-1)+3*ne)+3*nd+1, ((((nd+1)*3-1)+3*ne)+3*nd)+3*ne-1, 1, ne)
    curves['JoelhoE_trans'] = take(qjt, (((nd+1)*3-1)+3*ne)+3*nd+2, ((((nd+1)*3-1)+3*ne)+3*nd)+3*ne-1, 1, ne)
    curves['TornE_Sag'] = take(qjt, (((((nd+1)*3-1)+3*ne)+3*nd)+3*ne-1)+3*nd+1, ((((((nd+1)*3-1)+3*ne)+3*nd)+3*ne-1)+3*nd)+3*ne, 1, ne)
    curves['TornE_Trans'] = take(pp, ((nd*3+2)+3*ne-1)+3*nd+3, (((nd*3+2)+3*ne-1)+3*nd)+3*ne, 1, ne)
    return curves
