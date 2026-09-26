import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';
const dir=path.dirname(fileURLToPath(import.meta.url));
const root=path.dirname(dir);
const tables=JSON.parse(await fs.readFile(path.join(dir,'datos.json'),'utf8'));
const controls=JSON.parse(await fs.readFile(path.join(dir,'controles.json'),'utf8'));
const wb=Workbook.create();
const colors={navy:'#253A54',blue:'#426C91',orange:'#B66B28',pale:'#EEF3F7',text:'#243447'};
const col=n=>{let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
const dateVal=s=>new Date(s+'T00:00:00Z');
const cover=wb.worksheets.add('Inicio');
const control=wb.worksheets.add('Control_mensual');
for(const t of tables)wb.worksheets.add(t.nombre);
const dictionary=wb.worksheets.add('Diccionario');
const relations=wb.worksheets.add('Relaciones');
const practice=wb.worksheets.add('Practicas');

function base(sheet,range){
  sheet.showGridLines=false;
  sheet.getRange(range).format.font={name:'Arial',size:10,color:colors.text};
  sheet.getRange(range).format.verticalAlignment='center';
  sheet.getRange(range).format.rowHeight=21;
}
function header(sheet,range){
  sheet.getRange(range).format.fill=colors.navy;
  sheet.getRange(range).format.font={name:'Arial',size:10,bold:true,color:'#FFFFFF'};
  sheet.getRange(range).format.wrapText=true;
  sheet.getRange(range).format.horizontalAlignment='center';
  sheet.getRange(range).format.rowHeight=36;
}
function tabulate(sheet,headers,rows,name,widths){
  const end=col(headers.length-1), last=rows.length+1;
  sheet.getRange(`A1:${end}${last}`).values=[headers,...rows];
  base(sheet,`A1:${end}${last}`);
  sheet.tables.add(`A1:${end}${last}`,true,name);
  header(sheet,`A1:${end}1`);
  sheet.freezePanes.freezeRows(1);
  headers.forEach((h,i)=>sheet.getRange(`${col(i)}1:${col(i)}${last}`).format.columnWidth=widths?.[i]??20);
}

const intro=[
 ['Contenido','Valor','Uso en el curso'],
 ['Empresa','Farmacias Cóndor','Cadena ecuatoriana ficticia; datos íntegramente sintéticos.'],
 ['Edición','Curso 20260925','Esta edición sustituye la base mínima de 600 personas para los ejercicios del curso.'],
 ['Periodo','Enero 2023 – agosto 2026','44 meses completos de hechos. Calendario: años completos 2023 a 2026.'],
 ['Colaboradores',900,'Histórico de personas, sin reingresos.'],
 ['Activos al 31/08/2026',483,'Headcount al cierre, no total de registros históricos.'],
 ['Centros de trabajo',27,'24 farmacias, 2 centros de distribución y matriz; 12 ciudades, 4 regiones.'],
 ['Dimensiones',6,'Colaborador, área, cargo, sucursal, antigüedad y calendario.'],
 ['Hechos',5,'Plantilla mensual, movimientos, ausencias, contrataciones y capacitación.'],
 ['Importar en Power BI','Tablas dim_* y fact_*','Selecciona las tablas, no simultáneamente las hojas y las tablas de Excel.'],
 ['Power Query','raw_colaboradores','900 personas y 12 duplicados; espacios, categorías y fechas inconsistentes.'],
 ['Power Query','raw_plantilla','Muestra enero-febrero 2023; duplicados, fechas y decimales como texto.'],
 ['Fecha de salida','Primer día inactivo','Fecha vacía = persona activa al corte. No reemplazar por cero ni eliminar.'],
 ['Horas programadas','Ciclo simulado 5 de 7 días','8 horas por turno. Sin calendario legal de feriados. Denominador del ausentismo.'],
 ['Dinero','USD','Sueldos y costos didácticos. No calcula obligaciones legales ni liquidaciones.'],
 ['Historia organizativa','Asignación estable','Cada persona conserva área, cargo y centro. No se simulan traslados ni reingresos.'],
 ['Antigüedad','Histórica mensual','Tramo al último día activo del mes; misma clasificación en plantilla y eventos.'],
 ['Control de resultados','Control_mensual','Valores calculados desde las tablas; comparar después de cambiar de fuente.'],
 ['PostgreSQL','Esquema condor_curso','Los mismos datos en el SQL. Conserva el esquema condor anterior de Railway.'],
 ['CSV','Carpeta csv','UTF-8, coma como separador, punto decimal y fechas ISO YYYY-MM-DD.'],
 ['Modelo','Relaciones','Filtro unidireccional dimensión → hecho. No relacionar hechos entre sí.'],
 ['Origen de datos','Simulación, semilla 25092026','Las tendencias fueron diseñadas para ejercicios; no son evidencia sobre personas reales.'],
 ['Análisis predictivo','Ejercicio agregado','Practicar pronóstico mensual; sin predicciones reales ni decisiones individuales.'],
 ['Guía del curso','materiales/GUIA_DEL_CURSO.md','DAX, Power Query, ejercicios, dashboard y publicación.']
];
tabulate(cover,intro[0],intro.slice(1),'tbl_inicio',[30,36,108]);
cover.tabColor=colors.navy;
cover.getRange('C2:C24').format.wrapText=true;
cover.getRange('A2:C24').format.rowHeight=32;

for(const t of tables){
  const s=wb.worksheets.getItem(t.nombre), raw=t.nombre.startsWith('raw_');
  const rows=t.filas.map(row=>row.map((v,i)=>{
    if(v===null)return null;
    if(t.columnas[i].tipo==='date')return dateVal(v);
    if(raw && typeof v==='string' && /^\d{4}-\d{2}-\d{2}$/.test(v))return dateVal(v);
    return v;
  }));
  const widths=t.columnas.map(c=>c.nombre==='area'?32:c.nombre==='direccion'?24:c.nombre==='apellidos'?29:c.nombre==='sucursal'?36:c.nombre==='cargo'?34:c.nombre==='curso'?41:c.nombre==='tipo_ausencia'?26:c.nombre==='nivel_educativo'?23:c.nombre==='fecha_requisicion'?23:c.nombre.startsWith('fecha')?19:Math.max(17,Math.min(25,c.nombre.length+3)));
  tabulate(s,t.columnas.map(c=>c.nombre),rows,t.nombre,widths);
  if(raw)s.tabColor=colors.orange;
  else if(t.nombre==='dim_colaborador'||t.nombre==='fact_plantilla')s.tabColor=colors.blue;
  for(let i=0;i<t.columnas.length;i++){
    const c=t.columnas[i],r=s.getRange(`${col(i)}2:${col(i)}${rows.length+1}`);
    if(c.tipo==='date'||(raw && c.nombre.startsWith('fecha')))r.setNumberFormat('dd/mm/yyyy');
    else if(c.tipo==='numeric')r.setNumberFormat(c.nombre==='latitud'||c.nombre==='longitud'?'0.0000':'#,##0.00');
    else if(c.tipo==='integer')r.setNumberFormat('0');
  }
  console.log(`Preparada ${t.nombre}: ${rows.length}`);
}

const ctrlHeaders=['mes','hc_inicio','ingresos','salidas','hc_cierre','hc_promedio','rotacion','horas_programadas','horas_ausencia','indice_ausentismo','contrataciones','costo_contratacion_total','costo_por_contratacion','costo_personal_simulado'];
tabulate(control,ctrlHeaders,controls.map(r=>[dateVal(r[0]),...r.slice(1)]),'tbl_control_mensual',[17,17,17,17,17,18,17,23,21,23,21,27,26,28]);
const last=n=>tables.find(t=>t.nombre===n).filas.length+1;
const p=last('fact_plantilla'),m=last('fact_movimientos'),a=last('fact_ausencias'),c=last('fact_contrataciones');
const allFormulas=[];
for(let r=2;r<=45;r++){
  const mm=`$A${r}`,end=`EOMONTH(${mm},0)`;
  const values=[
    `=SUMIFS(fact_plantilla!$G$2:$G$${p},fact_plantilla!$A$2:$A$${p},${mm})`,
    `=COUNTIFS(fact_movimientos!$B$2:$B$${m},">="&${mm},fact_movimientos!$B$2:$B$${m},"<="&${end},fact_movimientos!$H$2:$H$${m},"Ingreso")`,
    `=COUNTIFS(fact_movimientos!$B$2:$B$${m},">="&${mm},fact_movimientos!$B$2:$B$${m},"<="&${end},fact_movimientos!$H$2:$H$${m},"Salida")`,
    `=SUMIFS(fact_plantilla!$H$2:$H$${p},fact_plantilla!$A$2:$A$${p},${mm})`,
    `=(B${r}+E${r})/2`, `=IF(F${r}=0,"",D${r}/F${r})`,
    `=SUMIFS(fact_plantilla!$J$2:$J$${p},fact_plantilla!$A$2:$A$${p},${mm})`,
    `=SUMIFS(fact_ausencias!$I$2:$I$${a},fact_ausencias!$B$2:$B$${a},">="&${mm},fact_ausencias!$B$2:$B$${a},"<="&${end})`,
    `=IF(H${r}=0,"",I${r}/H${r})`,
    `=COUNTIFS(fact_contrataciones!$B$2:$B$${c},">="&${mm},fact_contrataciones!$B$2:$B$${c},"<="&${end})`,
    `=SUMIFS(fact_contrataciones!$J$2:$J$${c},fact_contrataciones!$B$2:$B$${c},">="&${mm},fact_contrataciones!$B$2:$B$${c},"<="&${end})+SUMIFS(fact_contrataciones!$K$2:$K$${c},fact_contrataciones!$B$2:$B$${c},">="&${mm},fact_contrataciones!$B$2:$B$${c},"<="&${end})+SUMIFS(fact_contrataciones!$L$2:$L$${c},fact_contrataciones!$B$2:$B$${c},">="&${mm},fact_contrataciones!$B$2:$B$${c},"<="&${end})`,
    `=IF(K${r}=0,"",L${r}/K${r})`,
    `=SUMIFS(fact_plantilla!$L$2:$L$${p},fact_plantilla!$A$2:$A$${p},${mm})+SUMIFS(fact_plantilla!$N$2:$N$${p},fact_plantilla!$A$2:$A$${p},${mm})`
  ];
  allFormulas.push(values);
}
control.getRange('B2:N45').formulas=allFormulas;
control.getRange('A2:A45').setNumberFormat('mmm yyyy');
control.getRange('B2:E45').setNumberFormat('#,##0');
control.getRange('F2:F45').setNumberFormat('#,##0.0');
control.getRange('G2:G45').setNumberFormat('0.00%');
control.getRange('H2:I45').setNumberFormat('#,##0');
control.getRange('J2:J45').setNumberFormat('0.00%');
control.getRange('L2:N45').setNumberFormat('"$"#,##0.00');
control.tabColor=colors.navy;

const dict=[];
for(const t of tables)for(const c of t.columnas)dict.push([t.nombre,c.nombre,c.tipo,t.pk.includes(c.nombre)?'PK':t.fk[c.nombre]?'FK':'',c.descripcion]);
tabulate(dictionary,['tabla','campo','tipo','clave','descripcion'],dict,'tbl_diccionario',[26,27,16,12,110]);
dictionary.getRange(`E2:E${dict.length+1}`).format.wrapText=true;
dictionary.getRange(`A2:E${dict.length+1}`).format.rowHeight=29;
const rr=[];
for(const t of tables)for(const [campo,[dim,key]] of Object.entries(t.fk))rr.push([dim,key,t.nombre,campo,'1 a muchos','Única: dimensión a hecho','Sí']);
tabulate(relations,['dimension','clave_unica','hecho','clave_foranea','cardinalidad','direccion_filtro','activa'],rr,'tbl_relaciones',[25,24,26,24,18,33,13]);
const exercises=[
 ['01','Interfaz y flujo','Excel limpio','Importar → transformar → modelar → visualizar → publicar. Identificar cada vista.'],
 ['02','Tres fuentes','Excel, CSV, PostgreSQL','Conectar la misma tabla desde cada fuente. Comparar filas y controles; no anexar copias idénticas.'],
 ['03','Tipos y errores','raw_colaboradores','Quitar 12 duplicados; limpiar espacios; normalizar género; convertir fechas mixtas.'],
 ['04','Nulos','raw_colaboradores','Género nulo → No informado. Conservar fecha_salida vacía y notas pendientes.'],
 ['05','Decimales y fechas','raw_plantilla','Convertir sueldo con cultura es-EC, fechas dd/MM/yyyy e ISO; quitar 10 duplicados.'],
 ['06','Combinar consultas','fact_plantilla + dim_cargo','Left join por id_cargo; expandir cargo y nivel; comprobar que no aumentan filas.'],
 ['07','Combinar archivos','csv/movimientos_por_anio','Anexar los cuatro CSV por carpeta; resultado: 967 movimientos.'],
 ['08','Modelo estrella','Relaciones','Crear 30 relaciones activas de dimensiones a hechos. No unir hechos entre sí.'],
 ['09','Calendario','dim_calendario','Crear calendario en DAX como alternativa al importado. Elegir solo uno.'],
 ['10','Columnas y medidas','fact_contrataciones','Calcular días de cobertura y costos; diferenciar columna de medida.'],
 ['11','Headcount y rotación','fact_plantilla + movimientos','Agosto 2026: 486 iniciales + 11 ingresos − 14 salidas = 483 finales.'],
 ['12','Ausentismo y costo','ausencias + contrataciones','Agosto 2026: 2660/86112 horas; costo por contratación 1783.03/11 USD.'],
 ['13','Inteligencia de tiempo','44 meses','Comparar agosto 2026 vs julio 2026 y agosto 2025; ingresos acumulados al corte.'],
 ['14','Dashboard e interacción','Dimensiones y hechos','Tarjetas, líneas mensuales, barras por área, jerarquía región/ciudad/centro, tooltips.'],
 ['15','Storytelling','Control_mensual','Presentar problema, evidencia, hipótesis y acción; no atribuir causalidad a patrones simulados.'],
 ['16','Pronóstico e IA','Serie mensual agregada','Entrenar hasta febrero 2026 y contrastar marzo-agosto. Medir MAE frente a un pronóstico ingenuo.'],
 ['17','Publicación y actualización','Power BI Service','Publicar PBIX y configurar credenciales/orígenes; Excel local requiere acceso mediante gateway.']
];
tabulate(practice,['paso','tema','fuente','ejercicio'],exercises,'tbl_practicas',[12,28,35,112]);
practice.getRange('D2:D18').format.wrapText=true;
practice.getRange('A2:D18').format.rowHeight=34;
practice.tabColor='#7F8D99';dictionary.tabColor='#7F8D99';

wb.recalculate();
const obtained=control.getRange('B2:N45').values;
for(let i=0;i<44;i++)for(let j=0;j<13;j++){
  const target=controls[i][j+1],actual=obtained[i][j];
  if(typeof actual!=='number'||Math.abs(actual-target)>1e-6)throw new Error(`Control ${i},${j}: ${actual} != ${target}`);
}
console.log('44 controles mensuales coinciden con el cálculo independiente.');
console.log((await wb.inspect({kind:'table',range:'Control_mensual!A44:N45',include:'values,formulas',tableMaxRows:2,tableMaxCols:14,maxChars:1800})).ndjson);
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},maxChars:2000});
console.log(errors.ndjson);
await fs.mkdir(path.join(dir,'previews'),{recursive:true});
for(const name of ['Inicio','Control_mensual',...tables.map(t=>t.nombre),'Diccionario','Relaciones','Practicas']){
  const s=wb.worksheets.getItem(name);
  const table=tables.find(t=>t.nombre===s.name);
  const cols=table?table.columnas.length:s.name==='Control_mensual'?14:s.name==='Inicio'?3:s.name==='Diccionario'?5:s.name==='Relaciones'?7:4;
  const nrows=table?Math.min(8,table.filas.length+1):8;
  const preview=await wb.render({sheetName:s.name,range:`A1:${col(cols-1)}${nrows}`,scale:1,format:'png'});
  await fs.writeFile(path.join(dir,'previews',s.name+'.png'),new Uint8Array(await preview.arrayBuffer()));
}
const file=await SpreadsheetFile.exportXlsx(wb);
await file.save(path.join(root,'Farmacias_Condor_Curso.xlsx'));
console.log('Excel exportado.');
