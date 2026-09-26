from pathlib import Path
import json,csv
from decimal import Decimal
from collections import Counter

ROOT=Path(__file__).resolve().parent.parent
tables=json.loads((ROOT/'soporte/datos.json').read_text())
for t in tables:
    with (ROOT/'soporte/pg_export'/f"{t['nombre']}.csv").open(newline='') as f:
        rows=list(csv.reader(f))
    assert rows[0]==[c['nombre'] for c in t['columnas']],t['nombre']
    assert len(rows)-1==len(t['filas']),t['nombre']
    def canon(row):
        return tuple(None if v is None or v=='' else Decimal(str(v)) if c['tipo'] in ('integer','numeric') else str(v) for c,v in zip(t['columnas'],row))
    assert Counter(canon(r) for r in rows[1:])==Counter(canon(r) for r in t['filas']),t['nombre']
    print('PostgreSQL verificado:',t['nombre'],len(rows)-1)
controls=json.loads((ROOT/'soporte/controles.json').read_text())
with (ROOT/'soporte/pg_export/controles.csv').open(newline='') as f:actual=list(csv.reader(f))[1:]
assert len(actual)==44
for a,b in zip(actual,controls):
    assert a[0]==b[0]
    for x,y in zip(a[1:],b[1:]):assert abs(float(x)-y)<1e-6,(x,y)
print('44 controles mensuales SQL coinciden con los controles independientes.')
