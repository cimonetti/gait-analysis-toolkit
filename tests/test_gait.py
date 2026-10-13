import unittest
import numpy as np
from mapping import extract
from marcha import read_txt, ROOT, statistics
from revisao import identificar_ciclos, remover_ciclos

class Gait(unittest.TestCase):
    def test_columns_and_signs(self):
        # Independent expected block layout using two right and three left cycles.
        nd,ne=2,3
        qjt=np.tile(np.arange(1+9*(nd+ne)),(101,1))
        pp=np.tile(np.arange(1+6*(nd+ne)),(101,1))
        curves=extract(qjt,pp,nd,ne)
        for side,n,hip,knee,foot,pelvis,pfoot in [('D',nd,1,16,31,1,16),('E',ne,7,22,37,7,22)]:
            for suffix,k,sign in [('Sag',1,1),('Cor',0,-1 if side=='D' else 1),('Trans',2,1 if side=='D' else -1)]:
                np.testing.assert_equal(curves[f'Pelve{side}_{suffix}'][0],sign*np.arange(pelvis+k,pelvis+3*n,3))
            for seg,start in [('Quadril',hip),('Joelho',knee)]:
                for suffix,k in [('Sag',0),('Cor',1),('Trans' if seg=='Quadril' else 'trans',2)]:
                    np.testing.assert_equal(curves[f'{seg}{side}_{suffix}'][0],np.arange(start+k,start+3*n,3))
            np.testing.assert_equal(curves[f'Torn{side}_Sag'][0],np.arange(foot,foot+3*n,3))
            np.testing.assert_equal(curves[f'Torn{side}_Trans'][0],np.arange(pfoot+2,pfoot+3*n,3))
        self.assertEqual(len(curves),22)

    def test_exclusion_all_segments(self):
        record={'qjt':'examples/P01_001_QJT_E3D4.txt','pp':'examples/P01_001_PP_E3D4.txt','ciclos_d':4,'ciclos_e':3}
        curves=extract(read_txt(ROOT/record['qjt']),read_txt(ROOT/record['pp']),4,3)
        removed=remover_ciclos(curves,identificar_ciclos([record]),['D1','E2'])
        for key,values in removed.items():
            np.testing.assert_equal(values,curves[key][:,[1,2,3] if 'D_' in key else [0,2]])
        with self.assertRaises(ValueError): remover_ciclos(curves,identificar_ciclos([record]),['D1','D2','D3','D4'])

    def test_sample_statistics(self):
        mean,sd=statistics(np.tile([1.,3.],(101,1)))
        np.testing.assert_allclose(mean,2)
        np.testing.assert_allclose(sd,np.sqrt(2))

if __name__=='__main__': unittest.main()
