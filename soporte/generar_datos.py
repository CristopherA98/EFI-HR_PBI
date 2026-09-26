"""Una fuente reproducible para Excel, CSV y PostgreSQL. Datos sintéticos."""
from pathlib import Path
from datetime import date, timedelta
from calendar import monthrange
from collections import defaultdict, Counter
import random, math, csv, json, hashlib, copy

ROOT = Path(__file__).resolve().parent.parent
R = random.Random(25092026)
INICIO, CORTE = date(2023, 1, 1), date(2026, 8, 31)
TABLAS = {}

def tabla(nombre, columnas, grano, pk, fk=None, checks=None):
    t = dict(nombre=nombre, columnas=[dict(nombre=n, tipo=t, descripcion=d) for n,t,d in columnas],
             grano=grano, pk=pk, fk=fk or {}, checks=checks or [], filas=[])
    TABLAS[nombre] = t
    return t['filas']

def fechas(a,b):
    return [a+timedelta(days=i) for i in range((b-a).days+1)]

def azar_fecha(a,b):
    return a+timedelta(days=R.randint(0,(b-a).days))

def fin_mes(d):
    return date(d.year,d.month,monthrange(d.year,d.month)[1])

def tramo(dias):
    return 1 if dias<90 else 2 if dias<365 else 3 if dias<1095 else 4

areas = tabla('dim_area', [('id_area','integer','Clave única del área'),('area','text','Nombre del área'),('direccion','text','Dirección que agrupa el área')], 'Un área funcional', ['id_area'])
areas.extend([[1,'Operaciones de farmacia','Operaciones'],[2,'Logística','Operaciones'],[3,'Talento Humano','Soporte'],[4,'Finanzas','Soporte'],[5,'Tecnología','Soporte'],[6,'Comercial','Comercial']])
cargos = tabla('dim_cargo', [('id_cargo','integer','Clave única del cargo'),('cargo','text','Nombre del cargo'),('nivel','text','Nivel jerárquico'),('familia','text','Familia ocupacional')], 'Un cargo; área se registra en los hechos', ['id_cargo'])
CARGOS = [
 (1,'Auxiliar de farmacia','Operativo','Farmacia',1,620,.32),
 (2,'Cajero','Operativo','Farmacia',1,590,.38),
 (3,'Químico farmacéutico','Profesional','Farmacia',1,1250,.16),
 (4,'Jefe de farmacia','Jefatura','Farmacia',1,1100,.15),
 (5,'Asesor de servicio','Operativo','Farmacia',1,610,.36),
 (6,'Operario de bodega','Operativo','Logística',2,640,.27),
 (7,'Chofer repartidor','Operativo','Logística',2,790,.23),
 (8,'Supervisor de distribución','Jefatura','Logística',2,1300,.14),
 (9,'Analista de talento humano','Profesional','Administración',3,1200,.13),
 (10,'Jefe de talento humano','Jefatura','Administración',3,2100,.10),
 (11,'Analista contable','Profesional','Administración',4,1150,.13),
 (12,'Jefe financiero','Jefatura','Administración',4,2400,.09),
 (13,'Técnico de soporte','Profesional','Tecnología',5,1000,.16),
 (14,'Analista de datos','Profesional','Tecnología',5,1650,.16),
 (15,'Analista comercial','Profesional','Comercial',6,1200,.20),
 (16,'Agente de servicio telefónico','Operativo','Comercial',6,650,.42)]
cargos.extend([list(c[:4]) for c in CARGOS])
sedes = tabla('dim_sucursal', [('id_sucursal','integer','Clave única del centro'),('sucursal','text','Nombre ficticio del centro'),('ciudad','text','Ciudad de Ecuador'),('provincia','text','Provincia'),('region','text','Costa, Sierra, Amazonía o Insular'),('tipo_centro','text','Farmacia, CD o Matriz'),('latitud','numeric','Coordenada aproximada de la ciudad, no dirección real'),('longitud','numeric','Coordenada aproximada de la ciudad'),('fecha_apertura','date','Fecha ficticia anterior a las contrataciones')], 'Un centro de trabajo', ['id_sucursal'])
CIUDADES=[('Quito','Pichincha','Sierra',-.1807,-78.4678),('Guayaquil','Guayas','Costa',-2.1894,-79.8891),('Cuenca','Azuay','Sierra',-2.9001,-79.0059),('Manta','Manabí','Costa',-.9677,-80.7089),('Loja','Loja','Sierra',-3.9931,-79.2042),('Ambato','Tungurahua','Sierra',-1.2491,-78.6168),('Machala','El Oro','Costa',-3.2581,-79.9554),('Esmeraldas','Esmeraldas','Costa',.9682,-79.6517),('Tena','Napo','Amazonía',-.9938,-77.8129),('Nueva Loja','Sucumbíos','Amazonía',.0847,-76.8828),('Puerto Ayora','Galápagos','Insular',-.743,-90.313),('Riobamba','Chimborazo','Sierra',-1.6636,-78.6546)]
for ciudad,prov,reg,lat,lon in CIUDADES:
    for sector in ['Centro','Norte']:
        sedes.append([len(sedes)+1,f'Cóndor {ciudad} {sector}',ciudad,prov,reg,'Farmacia',lat,lon,date(2017,1,1)])
for nombre,idx,tipo in [('CD Quito',0,'CD'),('CD Guayaquil',1,'CD'),('Matriz Quito',0,'Matriz')]:
    ciudad,prov,reg,lat,lon=CIUDADES[idx]
    sedes.append([len(sedes)+1,nombre,ciudad,prov,reg,tipo,lat,lon,date(2017,1,1)])
ant = tabla('dim_antiguedad', [('id_antiguedad','integer','Clave del tramo'),('rango_antiguedad','text','Días cumplidos al último día activo del mes; misma clasificación en todos los hechos'),('orden','integer','Orden para el eje del gráfico')], 'Un tramo de antigüedad mensual', ['id_antiguedad'])
ant.extend([[1,'Menos de 90 días',1],[2,'90 a 364 días',2],[3,'365 a 1094 días',3],[4,'1095 días o más',4]])
cal = tabla('dim_calendario', [('fecha','date','Clave diaria sin huecos; 2023-2026 completos'),('anio','integer','Año calendario'),('trimestre','text','Trimestre calendario'),('mes','integer','Número del mes'),('mes_nombre','text','Nombre del mes en español'),('anio_mes','text','Etiqueta ordenable YYYY-MM'),('inicio_mes','date','Primer día del mes'),('fin_mes','date','Último día del mes'),('dia_semana','integer','Lunes=1, domingo=7')], 'Un día; incluye septiembre-diciembre de 2026 sin hechos', ['fecha'])
MESES=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
for d in fechas(INICIO,date(2026,12,31)):
    cal.append([d,d.year,f'T{(d.month-1)//3+1}',d.month,MESES[d.month-1],d.strftime('%Y-%m'),d.replace(day=1),fin_mes(d),d.isoweekday()])
colab=tabla('dim_colaborador', [('id_colaborador','integer','Persona única; sin reingresos en esta simulación'),('codigo','text','Identificador SIM, no cédula real'),('nombres','text','Nombre sintético'),('apellidos','text','Apellidos sintéticos'),('genero','text','Género simulado; No informado es una categoría válida'),('fecha_nacimiento','date','Fecha sintética, al menos 18 años al ingreso'),('fecha_ingreso','date','Primer día activo; puede ser anterior a 2023'),('fecha_salida','date','Primer día NO activo; vacío significa activo al corte'),('nivel_educativo','text','Nivel educativo ficticio'),('tipo_contrato','text','Contrato ficticio, no clasificación legal')], 'Una persona; atributos organizativos en los hechos', ['id_colaborador'], checks=['fecha_salida IS NULL OR fecha_salida > fecha_ingreso',"fecha_ingreso >= fecha_nacimiento + interval '18 years'"])
fk_comun={'id_colaborador':('dim_colaborador','id_colaborador'),'id_area':('dim_area','id_area'),'id_cargo':('dim_cargo','id_cargo'),'id_sucursal':('dim_sucursal','id_sucursal'),'id_antiguedad':('dim_antiguedad','id_antiguedad')}
CLAVES=[(k,'integer',f'Clave externa a {v[0]}') for k,v in fk_comun.items()]
plant=tabla('fact_plantilla', [('fecha','date','Inicio del mes; usar nivel mensual')]+CLAVES+[
 ('activo_inicio','integer','Activo justo antes de los movimientos del día 1; 0 o 1'),('activo_cierre','integer','Activo al finalizar el último día del mes; 0 o 1'),('dias_programados','integer','Turnos de 8 horas programados durante vínculo; ciclo simulado 5 de 7 días'),('horas_programadas','integer','Denominador de ausentismo; incluye horas luego ausentes'),('sueldo_mensual','numeric','USD de referencia mensual; no salario legal'),('pago_base','numeric','USD prorrateados por días calendario activos; ausencias no descuentan'),('horas_extra','integer','Horas extra simuladas, fuera del denominador de ausentismo'),('costo_extra','numeric','Costo didáctico: horas × sueldo/240 × 1.5')], 'Una persona por mes con vínculo o salida el día 1', ['fecha','id_colaborador'], {'fecha':('dim_calendario','fecha'),**fk_comun}, ['activo_inicio IN (0,1)','activo_cierre IN (0,1)','dias_programados BETWEEN 0 AND 31','horas_programadas = dias_programados * 8','pago_base >= 0','sueldo_mensual > 0','horas_extra >= 0','costo_extra >= 0'])
mov=tabla('fact_movimientos',[('id_movimiento','integer','Clave única'),('fecha','date','Día del ingreso o primer día inactivo')]+CLAVES+[('tipo_movimiento','text','Ingreso o Salida'),('motivo','text','Nueva contratación o motivo simulado de salida'),('salida_voluntaria','integer','1 para renuncia, 0 para los demás movimientos')], 'Un ingreso o una salida ocurridos desde enero de 2023', ['id_movimiento'], {'fecha':('dim_calendario','fecha'),**fk_comun}, ["tipo_movimiento IN ('Ingreso','Salida')",'salida_voluntaria IN (0,1)'])
aus=tabla('fact_ausencias',[('id_ausencia','integer','Clave única'),('fecha','date','Día de ausencia; turno programado dentro del vínculo')]+CLAVES+[('tipo_ausencia','text','Enfermedad, permiso o falta; excluye vacaciones'),('horas_ausencia','integer','4 u 8 horas; máximo un evento por persona/día'),('justificada','text','Sí o No')], 'Una ausencia parcial o total de un turno', ['id_ausencia'], {'fecha':('dim_calendario','fecha'),**fk_comun}, ['horas_ausencia IN (4,8)'])
contr=tabla('fact_contrataciones',[('id_vacante','integer','Proceso cubierto único; una persona contratada'),('fecha','date','Fecha de contratación e ingreso'),('fecha_requisicion','date','Apertura de la vacante; puede ser anterior a 2023')]+CLAVES+[('fuente','text','Canal de reclutamiento'),('costo_publicacion','numeric','USD del proceso cubierto'),('costo_evaluacion','numeric','USD de entrevistas/evaluación asignados al proceso'),('costo_agencia','numeric','USD de agencia, cero si no aplica'),('candidatos','integer','Personas postulantes; al menos una')], 'Un proceso cubierto de las contrataciones 2023-2026; excluye vacantes abiertas/canceladas', ['id_vacante'], {'fecha':('dim_calendario','fecha'),**fk_comun}, ['fecha_requisicion <= fecha','costo_publicacion >= 0','costo_evaluacion >= 0','costo_agencia >= 0','candidatos > 0'])
cap=tabla('fact_capacitacion',[('id_capacitacion','integer','Participación única'),('fecha','date','Fecha de capacitación dentro del vínculo')]+CLAVES+[('curso','text','Nombre del curso'),('modalidad','text','Virtual o Presencial'),('horas','integer','Horas de formación; subconjunto del tiempo programado'),('costo','numeric','USD de formación por participante'),('calificacion','numeric','Escala 0-100; nulo es pendiente, no cero')], 'Una participación en un curso, máximo una por persona/mes', ['id_capacitacion'], {'fecha':('dim_calendario','fecha'),**fk_comun}, ['horas > 0','costo >= 0','calificacion IS NULL OR calificacion BETWEEN 0 AND 100'])

PERSONAS={}
nombres_f=['Ana','María','Daniela','Valeria','Paola','Gabriela','Carolina','Isabel','Diana','Lucía','Andrea','Sofía']
nombres_m=['Luis','Carlos','José','Andrés','Diego','Juan','Pedro','Miguel','David','Jorge','Pablo','Santiago']
apellidos=['Paredes','Cevallos','Torres','Molina','Vera','Castro','Mendoza','Rojas','Flores','León','Ortiz','Silva','Zambrano','López','Sánchez','Ruiz','Vargas','Morales','Aguirre','Cabrera']
for i in range(1,901):
    ingreso=azar_fecha(date(2018,1,1),date(2022,12,31)) if i<=350 else azar_fecha(INICIO,CORTE)
    sitio=R.choices(['Farmacia','CD','Matriz'],[.82,.10,.08])[0]
    if sitio=='Farmacia':
        cargo=R.choices(CARGOS[:5],[.40,.22,.13,.10,.15])[0]
        sede=R.randint(1,24)
    elif sitio=='CD':
        cargo=R.choices(CARGOS[5:8],[.65,.25,.10])[0];sede=R.choice([25,26])
    else:
        cargo=R.choice(CARGOS[8:]);sede=27
    genero=R.choices(['Femenino','Masculino'],[.55,.45])[0]
    nombre=R.choice(nombres_f if genero=='Femenino' else nombres_m)
    if i%50==0: genero='No informado'
    nacimiento=ingreso-timedelta(days=R.randint(20*366,48*365))
    # Desde el inicio observado: los 350 iniciales están activos al 31/12/2022.
    origen=max(ingreso,INICIO)
    tasa=cargo[6]*(1.30 if sedes[sede-1][4]=='Costa' else .90)
    duracion=max(35,round(R.expovariate(tasa/365)))
    salida=origen+timedelta(days=duracion)
    if salida>CORTE: salida=None
    motivo=R.choices(['Renuncia','Fin de contrato','Desvinculación'],[.68,.22,.10])[0] if salida else None
    sueldo=round(cargo[5]*R.uniform(.95,1.18),2)
    colab.append([i,f'SIM-{i:05}',nombre,R.choice(apellidos)+' '+R.choice(apellidos),genero,nacimiento,ingreso,salida,R.choice(['Bachillerato','Técnico','Universitario','Posgrado']),R.choices(['Indefinido','Temporal'],[.85,.15])[0]])
    PERSONAS[i]=dict(ingreso=ingreso,salida=salida,area=cargo[4],cargo=cargo[0],sede=sede,sueldo=sueldo,motivo=motivo)

def claves(i,fecha):
    p=PERSONAS[i]
    referencia=min(fin_mes(fecha),p['salida']-timedelta(days=1) if p['salida'] else fin_mes(fecha))
    return [i,p['area'],p['cargo'],p['sede'],tramo(max(0,(referencia-p['ingreso']).days))]

for i,p in PERSONAS.items():
    ing,sal=p['ingreso'],p['salida']
    if ing>=INICIO:
        mov.append([len(mov)+1,ing]+claves(i,ing)+['Ingreso','Nueva contratación',0])
        canal=R.choices(['Portal de empleo','Referido','Universidad','Agencia'],[.48,.26,.18,.08])[0]
        dias=R.randint(9,35)+(15 if p['cargo'] in [3,10,12,14] else 0)
        contr.append([len(contr)+1,ing,ing-timedelta(days=dias)]+claves(i,ing)+[canal,round(R.uniform(25,90),2),round(R.uniform(60,160),2),round(R.uniform(350,900),2) if canal=='Agencia' else 0,R.randint(5,55)])
    if sal:
        mov.append([len(mov)+1,sal]+claves(i,sal)+['Salida',p['motivo'],int(p['motivo']=='Renuncia')])

meses=[date(y,m,1) for y in range(2023,2027) for m in range(1,13) if date(y,m,1)<=CORTE]
for m in meses:
    fin=fin_mes(m)
    for i,p in PERSONAS.items():
        ing,sal=p['ingreso'],p['salida']
        if ing>fin or (sal and sal<m):continue
        ultimo=min(fin,sal-timedelta(days=1) if sal else fin)
        dias=fechas(max(m,ing),ultimo)
        programados=[d for d in dias if (d.toordinal()+i)%7<5]
        referencia=max(ing,ultimo)
        sueldo=round(p['sueldo']*(1.035**(m.year-2023)),2)
        extra=R.choices([0,4,8,12,16],[.44,.23,.18,.10,.05])[0] if programados else 0
        plant.append([m]+claves(i,referencia)+[int(ing<m and (sal is None or sal>=m)),int(ing<=fin and (sal is None or sal>fin)),len(programados),len(programados)*8,sueldo,round(sueldo*len(dias)/fin.day,2),extra,round(extra*sueldo/240*1.5,2)])
        ocupados=set()
        for d in programados:
            tasa=.032*(1.4 if p['sede'] in [3,4,7,8,15,16] else 1)*(1.25 if d.month in [6,7] else 1)
            if R.random()<tasa:
                tipo=R.choices(['Enfermedad','Permiso personal','Falta injustificada'],[.62,.28,.10])[0]
                aus.append([len(aus)+1,d]+claves(i,d)+[tipo,R.choices([4,8],[.25,.75])[0],'No' if tipo=='Falta injustificada' else 'Sí'])
                ocupados.add(d)
        disponibles=[d for d in programados if d not in ocupados]
        if disponibles and R.random()<.19:
            d=R.choice(disponibles)
            cap.append([len(cap)+1,d]+claves(i,d)+[R.choice(['Atención al cliente','Buenas prácticas de almacenamiento','Seguridad ocupacional','Excel y análisis de datos','Liderazgo de equipos']),R.choice(['Virtual','Presencial']),R.choice([2,4,8]),round(R.uniform(15,90),2),None if d>=date(2026,8,1) and R.random()<.2 else round(max(40,min(100,R.gauss(82,9))),1)])

# Fuente sucia recuperable: no se inventa información para completar género.
raw_c=tabla('raw_colaboradores',[(c['nombre'],'text','Entrada de práctica; corregir según diccionario de dim_colaborador') for c in TABLAS['dim_colaborador']['columnas']], '900 personas más 12 duplicados exactos; no cargar al modelo final', [])
raw_c.extend(copy.deepcopy(colab))
for n,row in enumerate(raw_c):
    if n<30: row[3]='  '+row[3]+'  '
    if 30<=n<60:row[4]=row[4].lower()
    if colab[n][4]=='No informado':row[4]=None
    if 60<=n<80:row[6]=row[6].strftime('%d/%m/%Y')
raw_c.extend(copy.deepcopy(raw_c[100:112]))
raw_p=tabla('raw_plantilla',[(c['nombre'],'text','Entrada de práctica; corregir según diccionario de fact_plantilla') for c in TABLAS['fact_plantilla']['columnas']], 'Primeros dos meses completos más 10 duplicados exactos; muestra de práctica', [])
raw_p.extend(copy.deepcopy([row for row in plant if row[0]<date(2023,3,1)]))
for row in raw_p[:25]:row[10]=f'{row[10]:.2f}'.replace('.',',')
for row in raw_p[25:40]:row[0]=row[0].strftime('%d/%m/%Y')
raw_p.extend(copy.deepcopy(raw_p[60:70]))

# Tipos raw se conservan mezclados en Excel; CSV/PostgreSQL raw son texto.
def ser(v):return v.isoformat() if isinstance(v,date) else v
def quote(v):
    if v is None:return 'NULL'
    if isinstance(v,(float,int)):return str(v)
    return "'"+str(ser(v)).replace("'","''")+"'"
def sqltype(c, raw):
    if raw:return 'text'
    return {'integer':'integer','text':'text','date':'date','numeric':'numeric(14,4)' if c['nombre'] in ['latitud','longitud'] else 'numeric(14,2)'}[c['tipo']]

sql=['-- Farmacias Cóndor / edición curso 20260925 / semilla 25092026',
     '-- Datos 100% ficticios. Esquema nuevo: no modifica condor ni public.',
     '-- Si condor_curso ya existe, se aborta; no elimina tablas.', 'BEGIN;','CREATE SCHEMA condor_curso;']
manifest={}
for name,t in TABLAS.items():
    path=ROOT/'csv'/f'{name}.csv'
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow([c['nombre'] for c in t['columnas']]);w.writerows([[ser(v) for v in row] for row in t['filas']])
    manifest[name]=dict(filas=len(t['filas']),sha256_csv=hashlib.sha256(path.read_bytes()).hexdigest())
    raw=name.startswith('raw_')
    nullable={'fecha_salida','calificacion'}
    defs=[f"{c['nombre']} {sqltype(c,raw)}"+('' if raw or c['nombre'] in nullable else ' NOT NULL') for c in t['columnas']]
    if t['pk']:defs.append('PRIMARY KEY ('+', '.join(t['pk'])+')')
    for k,(ref,rc) in t['fk'].items():defs.append(f'FOREIGN KEY ({k}) REFERENCES condor_curso.{ref} ({rc})')
    defs += ['CHECK ('+ch+')' for ch in t['checks']]
    if name=='fact_ausencias':defs.append('UNIQUE (id_colaborador, fecha)')
    if name=='fact_contrataciones':defs.append('UNIQUE (id_colaborador)')
    sql.append(f'CREATE TABLE condor_curso.{name} (\n  '+',\n  '.join(defs)+'\n);')
    sql.append(f'COMMENT ON TABLE condor_curso.{name} IS {quote(t["grano"])};')
    for c in t['columnas']:sql.append(f'COMMENT ON COLUMN condor_curso.{name}.{c["nombre"]} IS {quote(c["descripcion"])};')
    for j in range(0,len(t['filas']),400):
        rows=t['filas'][j:j+400]
        if raw:rows=[[None if v is None else str(ser(v)) for v in row] for row in rows]
        sql.append(f'INSERT INTO condor_curso.{name} VALUES\n'+',\n'.join('('+','.join(quote(v) for v in row)+')' for row in rows)+';')
    for k in t['fk']:
        if not t['pk'] or t['pk'][0]!=k:sql.append(f'CREATE INDEX ix_{name}_{k} ON condor_curso.{name} ({k});')
sql += ['COMMIT;']
sql += [f"SELECT '{name}' AS tabla, count(*) AS filas FROM condor_curso.{name};" for name in TABLAS]
(ROOT/'postgresql'/'01_crear_condor_curso.sql').write_text('\n'.join(sql)+'\n')
(ROOT/'soporte'/'datos.json').write_text(json.dumps(list(TABLAS.values()),ensure_ascii=False,default=ser))
(ROOT/'soporte'/'manifest.json').write_text(json.dumps(manifest,indent=2))

# Particiones para la práctica Combinar archivos de carpeta.
partdir=ROOT/'csv'/'movimientos_por_anio';partdir.mkdir(exist_ok=True)
for y in range(2023,2027):
    with (partdir/f'movimientos_{y}.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow([c['nombre'] for c in TABLAS['fact_movimientos']['columnas']]);w.writerows([[ser(v) for v in row] for row in mov if row[1].year==y])

# Validaciones de claves, fechas y coherencia entre hechos.
for name,t in TABLAS.items():
    idx={c['nombre']:i for i,c in enumerate(t['columnas'])}
    if t['pk']:
        keys=[tuple(r[idx[c]] for c in t['pk']) for r in t['filas']]
        assert len(keys)==len(set(keys)),name
    for k,(ref,rc) in t['fk'].items():
        rix=[c['nombre'] for c in TABLAS[ref]['columnas']].index(rc)
        valid={r[rix] for r in TABLAS[ref]['filas']}
        assert all(r[idx[k]] in valid for r in t['filas']), (name,k)
aus_horas=defaultdict(int)
for r in aus:
    p=PERSONAS[r[2]]
    assert r[1]>=p['ingreso'] and (not p['salida'] or r[1]<p['salida'])
    assert (r[1].toordinal()+r[2])%7<5
    aus_horas[r[1].replace(day=1),r[2]]+=r[8]
for r in plant:assert aus_horas[r[0],r[1]]<=r[9]
clave_mes={(r[0],r[1]):r[1:6] for r in plant}
for filas in [aus,mov,cap]:
    for r in filas:assert r[2:7]==clave_mes[r[1].replace(day=1),r[2]]
for r in contr:assert r[3:8]==clave_mes[r[1].replace(day=1),r[3]]
for r in cap:
    p=PERSONAS[r[2]]
    assert r[1]>=p['ingreso'] and (not p['salida'] or r[1]<p['salida'])
assert {r[3] for r in contr}=={r[2] for r in mov if r[7]=='Ingreso'}

controles=[]
for m in meses:
    pr=[r for r in plant if r[0]==m]
    mr=[r for r in mov if r[1].replace(day=1)==m]
    cr=[r for r in contr if r[1].replace(day=1)==m]
    ini=sum(r[6] for r in pr);fin=sum(r[7] for r in pr)
    ingresos=sum(r[7]=='Ingreso' for r in mr);salidas=sum(r[7]=='Salida' for r in mr)
    assert ini+ingresos-salidas==fin, m
    esperado=sum(p['ingreso']<=fin_mes(m) and (p['salida'] is None or p['salida']>fin_mes(m)) for p in PERSONAS.values())
    assert fin==esperado
    prom=(ini+fin)/2
    hp=sum(r[9] for r in pr);ha=sum(v for (mm,i),v in aus_horas.items() if mm==m)
    cc=round(sum(sum(r[9:12]) for r in cr),2)
    controles.append([m,ini,ingresos,salidas,fin,prom,salidas/prom if prom else None,hp,ha,ha/hp if hp else None,len(cr),cc,cc/len(cr) if cr else None,round(sum(r[11]+r[13] for r in pr),2)])
(ROOT/'soporte'/'controles.json').write_text(json.dumps(controles,default=ser))
print(json.dumps({'tablas':manifest,'ultimo_mes':controles[-1],'validaciones':'claves, relaciones, fechas, horas y balance de 44 meses correctos'},ensure_ascii=False,indent=2,default=ser))
