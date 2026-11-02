import unittest
from decimal import Decimal
from pathlib import Path
from normalizacion import cargar_reglas, leer_json, exportar_json
from validacion import procesar
from metricas import calcular

class Pruebas(unittest.TestCase):
    def setUp(self):
        self.r = cargar_reglas()
        self.d = leer_json((Path(__file__).resolve().parents[1]/'datos/transacciones_mixtas.json').read_text())
    def test_lote_y_metricas(self):
        v,i = procesar(self.d,self.r)
        self.assertEqual((len(v),len(i)),(5,10))
        m = calcular(v,i)
        self.assertEqual(m['por_moneda'],{'USD':Decimal('201.30'),'EUR':Decimal('99.99')})
        self.assertEqual(m['por_estado'],{'SUCCESS':3,'PENDING':1,'FAILED':1})
        self.assertEqual(v[1]['amount'],Decimal('100.50'))
    def test_zonas(self):
        v,_ = procesar(self.d,self.r)
        self.assertEqual(v[0]['timestamp'],'2025-03-10T20:22:00+00:00')
        self.assertEqual(v[2]['timestamp'],'2025-03-10T14:22:00+00:00')
    def test_precision_exportacion(self):
        x = Decimal('123456789012345.123456789')
        self.assertEqual(leer_json(exportar_json([{'amount':x}]))[0]['amount'],x)
    def test_raiz_y_json(self):
        for texto in ['{}','[','[NaN]']:
            with self.assertRaises(ValueError): leer_json(texto)
    def test_vacio(self):
        self.assertEqual(calcular(*procesar([],self.r))['procesadas'],0)
    def test_ambigua(self):
        t = dict(self.d[0],ref='otro')
        v,i = procesar([t],self.r)
        self.assertFalse(v);self.assertIn('ambigua',i[0]['motivo'])
    def test_politica_configurable(self):
        t = dict(self.d[0],amount='0')
        self.r['permitir_cero']=True
        self.assertEqual(len(procesar([t],self.r)[0]),1)

if __name__=='__main__': unittest.main()
