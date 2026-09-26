from pathlib import Path
from datetime import date,datetime
import json,csv,math
from openpyxl import load_workbook
from PIL import Image,ImageOps,ImageDraw

ROOT=Path(__file__).resolve().parent.parent
tables=json.loads((ROOT/'soporte/datos.json').read_text())
controls=json.loads((ROOT/'soporte/controles.json').read_text())
w=load_workbook(ROOT/'Farmacias_Condor_Curso.xlsx',read_only=True,data_only=True)

def norm(x):
    if isinstance(x,(date,datetime)):return x.strftime('%Y-%m-%d')
    return x

for t in tables:
    s=w[t['nombre']]
    actual=list(s.values)
    assert actual[0]==tuple(c['nombre'] for c in t['columnas']),t['nombre']
    assert len(actual)-1==len(t['filas']),t['nombre']
    for n,(a,b) in enumerate(zip(actual[1:],t['filas'])):
        for j,(x,y) in enumerate(zip(a,b)):
            x=norm(x)
            if isinstance(y,(int,float)):
                assert isinstance(x,(int,float)) and abs(x-y)<1e-8,(t['nombre'],n,j,x,y)
            else:assert x==y,(t['nombre'],n,j,x,y)
    with (ROOT/'csv'/f"{t['nombre']}.csv").open(encoding='utf-8-sig',newline='') as f:
        lines=list(csv.reader(f))
    assert lines[0]==[c['nombre'] for c in t['columnas']]
    assert lines[1:]==[[str(v) if v is not None else '' for v in row] for row in t['filas']]
    print('Excel/CSV verificados:',t['nombre'],len(actual)-1)

for a,b in zip(list(w['Control_mensual'].values)[1:],controls):
    assert norm(a[0])==b[0]
    for x,y in zip(a[1:],b[1:]):assert isinstance(x,(int,float)) and abs(x-y)<1e-6,(x,y)
assert sum(r[7] is None for r in tables[5]['filas'])==483

# Recuperación completa de los ejercicios raw, con las reglas de Power Query.
clean={t['nombre']:t['filas'] for t in tables}
seen=set();restored=[]
for row in clean['raw_colaboradores']:
    if tuple(row) in seen:continue
    seen.add(tuple(row));r=row.copy()
    r[3]=r[3].strip()
    r[4]='No informado' if r[4] is None else {'femenino':'Femenino','masculino':'Masculino','no informado':'No informado'}[r[4].strip().lower()]
    if '/' in r[6]:r[6]=datetime.strptime(r[6],'%d/%m/%Y').strftime('%Y-%m-%d')
    restored.append(r)
assert restored==clean['dim_colaborador']
seen=set();restored=[]
for row in clean['raw_plantilla']:
    if tuple(row) in seen:continue
    seen.add(tuple(row));r=row.copy()
    if '/' in r[0]:r[0]=datetime.strptime(r[0],'%d/%m/%Y').strftime('%Y-%m-%d')
    if isinstance(r[10],str):r[10]=float(r[10].replace(',','.'))
    restored.append(r)
assert restored==[r for r in clean['fact_plantilla'] if r[0]<'2023-03-01']
print('Controles guardados y recuperación de fuentes raw: correctos.')

# Exportación de PostgreSQL para verificar todos los valores, no solo conteos.
pgdir=ROOT/'soporte/pg_export';pgdir.mkdir(exist_ok=True)
sql=[]
for t in tables:
    file=str(pgdir/(t['nombre']+'.csv')).replace("'","''")
    sql.append(f"COPY condor_curso.{t['nombre']} TO '{file}' WITH (FORMAT CSV, HEADER TRUE);")
q=(ROOT/'postgresql/02_verificar.sql').read_text().split('WITH p AS (',1)[1]
q='WITH p AS ('+q.strip().rstrip(';')
file=str(pgdir/'controles.csv').replace("'","''")
sql.append(f"COPY ({q}) TO '{file}' WITH (FORMAT CSV, HEADER TRUE);")
(ROOT/'soporte/exportar_pg.sql').write_text('\n'.join(sql)+'\n')

# Contact sheets para revisión visual de todas las pestañas renderizadas.
images=sorted((ROOT/'soporte/previews').glob('*.png'))
for n in range(0,len(images),6):
    canvas=Image.new('RGB',(1800,1050),'#e7ecf1')
    draw=ImageDraw.Draw(canvas)
    for k,p in enumerate(images[n:n+6]):
        im=Image.open(p).convert('RGB')
        im.thumbnail((870,295))
        x=15+(k%2)*900;y=12+(k//2)*350
        draw.text((x,y),p.stem,fill='black')
        canvas.paste(im,(x,y+28))
    canvas.save(ROOT/'soporte'/f'contacto_{n//6+1}.png')
