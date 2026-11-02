from collections import Counter
from decimal import Decimal

def calcular(validas, invalidas):
    totales = {}
    for t in validas:
        totales[t['currency']] = totales.get(t['currency'], Decimal('0')) + t['amount']
    return {'procesadas':len(validas)+len(invalidas),'validas':len(validas),'invalidas':len(invalidas),
            'por_estado':dict(Counter(t['status'] for t in validas)), 'por_moneda':totales}
