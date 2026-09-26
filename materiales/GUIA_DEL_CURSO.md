# Farmacias Cóndor: práctica de Power BI

Edición Curso 20260925. Cadena ficticia ecuatoriana con 24 farmacias, dos centros de distribución y una matriz. Datos sintéticos de 900 personas y 44 meses de hechos, enero de 2023 a agosto de 2026. La edición inicial de 600 colaboradores permanece separada: sus cifras no sirven como control de esta edición.

## Comenzar con Excel

1. Copia `Farmacias_Condor_Curso.xlsx` a una carpeta de Windows, por ejemplo `C:\CursoPowerBI`. No requiere conexión a Railway ni instalaciones adicionales.
2. En Power BI Desktop: Obtener datos → Libro de Excel. Selecciona las tablas `dim_*` y `fact_*`; evita seleccionar también las hojas del mismo nombre.
3. Pulsa Transformar datos. Revisa tipos y nombres, luego Cerrar y aplicar.
4. Crea las relaciones de la hoja Relaciones. Oculta las claves del panel de campos del informe, sin eliminarlas.
5. Crea las medidas de `MEDIDAS_DAX.txt` una a una. Empieza con una matriz por `dim_calendario[anio_mes]` y contrasta con Control_mensual.

La hoja Inicio orienta el trabajo; Diccionario explica todos los campos. Control_mensual, Relaciones y Practicas son material de apoyo, no tablas del modelo. Las hojas raw son ejercicios de limpieza, tampoco se cargan junto a sus equivalentes limpios.

## Conectar tres fuentes equivalentes

| Fuente | Ruta | Resultado esperado |
|---|---|---|
| Excel | Tablas del libro | 11 tablas analíticas |
| CSV | Un archivo por tabla, carpeta csv | Mismos nombres, filas y valores |
| PostgreSQL | Esquema condor_curso tras ejecutar el SQL | Misma edición, claves y restricciones |

Los CSV tienen codificación UTF-8, delimitador coma, punto decimal y fechas ISO. En Power Query utiliza cultura Inglés (Estados Unidos) para decimales de los CSV limpios, y tipo Fecha para columnas de fecha. Los vacíos representan nulos. PostgreSQL conserva fechas y números tipados.

Práctica sencilla: carga `dim_sucursal` desde cada fuente, compara sus 27 filas y luego conserva una sola consulta con el nombre final. Práctica mixta: dimensiones desde Excel, movimientos desde CSV y hechos restantes desde PostgreSQL. Las claves son iguales. **No anexes Excel y PostgreSQL cuando contienen copias de los mismos registros**: duplicarías indicadores.

Para alternar el origen conservando medidas, edita los pasos Origen/Navegación de una consulta existente; conserva nombre, columnas y tipos. Los parámetros ayudan a cambiar ruta, servidor y base. El modelo no necesita rediseñarse.

## Power Query: errores deliberados

### raw_colaboradores

Entrada: 912 filas. Salida: 900 personas, iguales a dim_colaborador.

1. Mantén la consulta como ejercicio separado; elimina el paso automático Tipo cambiado si produce errores.
2. Quita duplicados exactos en todas las columnas: son 12 copias. En una base real, investiga diferencias antes de deduplicar solo por identificador.
3. Aplica Limpiar y Recortar a nombres/apellidos. Hay 30 apellidos con espacios exteriores.
4. Normaliza género: `femenino` → `Femenino`, `masculino` → `Masculino`, nulo → `No informado`. Los 18 nulos son ausencia de información, no se infiere el género a partir del nombre.
5. Convierte identificador a entero; fechas a Fecha. Veinte fechas de ingreso están como texto dd/MM/yyyy, el resto son fechas reales en Excel. Usa la función M auxiliar del archivo POWER_QUERY.txt si mezclas los CSV y PostgreSQL raw.
6. Conserva las fechas de salida nulas: son 483 personas activas al corte. No reemplazarlas por una fecha inventada.
7. Crea Nombre completo con una columna personalizada: `[nombres] & " " & [apellidos]`.

### raw_plantilla

Entrada: 761 filas; después de quitar 10 duplicados quedan 751 registros de enero-febrero 2023. Es una muestra para limpieza, **no reemplaza las 18.961 filas históricas de fact_plantilla**.

Veinticinco sueldos están como texto con coma decimal y quince fechas como texto dd/MM/yyyy. Convierte sueldos con la cultura es-EC solo si son texto; conserva los valores numéricos. Después establece Fecha, Entero y Decimal en sus columnas correspondientes. No borres registros con activo_cierre = 0: representan salidas o movimientos del mes.

### Combinar tablas y archivos

- Combina fact_plantilla con dim_cargo por id_cargo, unión izquierda. Expande cargo y nivel. Deben seguir siendo 18.961 filas. Úsalo como ejercicio; en el modelo final la relación evita repetir atributos.
- Combina los cuatro archivos de `csv/movimientos_por_anio` con el conector Carpeta. Deben resultar 967 movimientos. No incluyas también el CSV consolidado.
- Agrupa fact_ausencias por persona e inicio de mes y suma horas. Solo entonces combina ese resumen con fact_plantilla por ambas claves. La unión de eventos sin agrupar multiplicaría la nómina mensual.

## Estructura y modelo estrella

Cada tabla de hechos tiene las seis claves dimensionales: fecha, colaborador, área, cargo, sucursal y antigüedad. Las cinco tablas comparten dimensiones conformadas. La hoja Relaciones contiene las 30 relaciones, activas, de uno a muchos y con filtro en un solo sentido, dimensión → hecho.

| Tabla de hechos | Una fila representa |
|---|---|
| fact_plantilla | Persona y mes con vínculo o salida el primer día |
| fact_movimientos | Ingreso o salida desde 2023 |
| fact_ausencias | Ausencia de 4 u 8 horas en un turno programado |
| fact_contrataciones | Proceso cubierto y persona contratada |
| fact_capacitacion | Participación individual en un curso |

No relaciones hechos entre sí. No crees relaciones de dim_colaborador a otras dimensiones: las claves organizativas pertenecen a los hechos. No relaciones activamente fecha_ingreso/fecha_salida de dim_colaborador al calendario; se analizan mediante fact_movimientos.

Las asignaciones organizativas son estables en esta simulación. Las claves ya están repetidas en cada hecho para practicar el esquema estrella y permitir una futura historia de cambios. No se simulan reingresos; en un caso real se necesitaría una clave de contrato/episodio.

## Calendario y periodos

Importa dim_calendario o créala con la expresión DAX entregada, nunca ambas. Sus 1.461 fechas son únicas, consecutivas y cubren cuatro años completos. Marca la tabla de fechas; ordena mes_nombre por mes. Desactiva la creación automática de tablas de fecha para este archivo.

Filtra el informe a enero de 2023–agosto de 2026. Los meses restantes de 2026 sirven para completar el calendario y no contienen hechos. La plantilla está fechada el primer día del mes: usa segmentadores mensuales y evita mezclar headcount mensual con filtros de días sueltos.

## Definiciones que deben explicarse

- Fecha de ingreso: primer día activo. Fecha de salida: primer día no activo. Un empleado que sale el 1 de agosto forma parte del headcount inicial, se cuenta como salida y no tiene horas programadas en agosto.
- Headcount inicial: antes de los movimientos del primer día. Headcount final: al cierre del último día. Control: inicial + ingresos − salidas = final.
- Rotación mensual: salidas / promedio de plantilla inicial y final. Para varios meses: salidas del periodo / promedio de las plantillas medias mensuales. No sumar porcentajes mensuales ni anualizar sin explicarlo.
- Ausentismo: horas de ausencia / horas programadas. Programación simulada de ocho horas, cinco días de cada siete, con turnos rotativos; incluye las horas luego ausentes y excluye horas extra. No incluye vacaciones ni calendario legal de feriados.
- Costo por contratación: costos de publicación, evaluación y agencia de procesos cubiertos / contrataciones de esos procesos. No incluye vacantes abiertas ni canceladas.
- Sueldo y pago: USD simulados, sin cálculo legal de nómina. Pago base proporcional a días calendario activos. Las ausencias no descuentan el pago. Costo extra = horas extra × sueldo/240 × 1,5, supuesto didáctico.
- Antigüedad: tramo al último día activo del mes, aplicado a todos los hechos de la persona en ese mes. Esto alinea numeradores y denominadores al segmentar. Los eventos no usan la antigüedad exacta del día del evento. Entre meses las personas cambian de tramo: el balance de varios meses por antigüedad requiere contabilizar esas transiciones; para conciliación de periodos utiliza total, área, cargo, género o ubicación.
- Notas de capacitación vacías: pendientes de evaluación; no equivalen a cero.

## Secuencia de DAX y valores de control

Crear primero columnas Nombre completo, Dias cobertura y Costo proceso. Continuar con SUM, COUNTROWS, DISTINCTCOUNT y AVERAGE; después CALCULATE, filtros, SUMX, medidas de stock y de flujo, DATEADD, SAMEPERIODLASTYEAR y DATESYTD.

Una columna se evalúa por fila al procesar el modelo; una medida responde al contexto del visual. Demostrar con el mismo costo por contratación en tarjetas globales, por área y por canal. No promediar promedios: dividir el costo total entre el número de procesos del contexto.

Control de agosto 2026, sin otros filtros:

| Indicador | Resultado |
|---|---:|
| Headcount inicial | 486 |
| Ingresos / salidas | 11 / 14 |
| Headcount final | 483 |
| Headcount promedio | 484,5 |
| Rotación mensual | 2,8896 % |
| Horas programadas / ausentes | 86.112 / 2.660 |
| Índice de ausentismo | 3,0890 % |
| Contrataciones | 11 |
| Costo total de contratación | USD 1.783,03 |
| Costo por contratación | USD 162,09 |
| Costo de personal simulado | USD 511.116,36 |

Usa Control_mensual para comprobar los 44 meses. Los controles se calculan con fórmulas de Excel y se contrastan con cálculos independientes. Las medidas DAX se entregan como material de práctica; deben ejecutarse en Power BI para validar su comportamiento en el modelo.

## Dashboard, interacción y relato

Página 1, Resumen ejecutivo: tarjetas de headcount final, rotación, ausentismo y costo por contratación; línea de plantilla mensual; barras de salidas por área. Segmentadores de año-mes, área, cargo, género, tramo de antigüedad y región. Mostrar el periodo analizado en el título.

Página 2, Operación: matriz por sucursal con horas programadas, horas ausentes y tasa; barras ordenadas por tasa acompañadas del denominador. Jerarquía región → provincia → ciudad → sucursal para drill-down. Tooltip con headcount y horas evita interpretar una tasa sin tamaño de población. Configura latitud y longitud como coordenadas si utilizas mapas; son centros de ciudad aproximados.

Página 3, Atracción y desarrollo: costo y días de cobertura por fuente, participantes y horas de formación por área. Usa tooltips y drill-through para el detalle del proceso o centro. Revisa Editar interacciones: selección de una fuente de reclutamiento no tiene por qué filtrar la plantilla si esa fuente existe solo en contrataciones.

Errores a discutir: sumar headcount de varios meses, usar 900 históricos como activos, calcular rotación sobre ingresados, mezclar días calendario con horas de ausencia, unir hechos sin agrupar, promediar porcentajes, usar solo colores sin etiquetas y comparar 2026 parcial contra todo 2025.

Relato de ejemplo: en agosto la plantilla pasa de 486 a 483 porque hubo 11 ingresos y 14 salidas. Antes de proponer acciones, segmentar áreas y centros, revisar tendencias y formular hipótesis. Las diferencias de esta simulación son patrones diseñados, no evidencia causal.

## Analítica predictiva e IA

Ejercicio de pronóstico agregado, sin identificar ni clasificar personas:

1. Crea una línea de costo de personal o headcount por fecha mensual continua, una sola serie y sin leyenda categórica.
2. Reserva marzo–agosto de 2026 como prueba temporal. Entrena solo con enero de 2023–febrero de 2026.
3. En el panel Analítica, cuando esté disponible en el visual, agrega seis meses de pronóstico y un intervalo de confianza. Compáralo con valores reales reservados.
4. Calcula MAE = promedio de ABS(real − pronóstico). Compara contra la referencia ingenua: repetir el último valor conocido. No entrenes con el periodo de prueba.
5. Explica que 44 meses y un proceso sintético sirven para aprender, no para validar una política real de personal.

Para IA descriptiva, usa Influenciadores clave en modo Importar sobre una copia de fact_plantilla enriquecida con cargo y región, analizando horas_extra. No incluyas costo_extra como explicador porque deriva de horas_extra. No conectes esa copia al modelo principal. La asociación no demuestra causalidad. No se requiere Copilot ni un servicio de IA de pago para este ejercicio.

## Publicación y actualización

1. Guarda el PBIX y publícalo en un espacio de trabajo autorizado del Servicio. La cuenta y licencia necesarias dependen del espacio y de cómo se comparta.
2. Configura conexiones y credenciales del modelo semántico. Ejecuta Actualizar ahora y revisa su historial antes de programar horarios.
3. Excel/CSV locales requieren una puerta de enlace con acceso a sus rutas. Si los archivos están dentro de Windows en Parallels, Windows y la puerta de enlace deben permanecer disponibles.
4. Para evitar una ruta local, una alternativa es usar OneDrive empresarial/SharePoint mediante su conector, no una ruta sincronizada del Mac. Esto requiere una cuenta y configuración apropiadas.
5. PostgreSQL puede conectarse mediante conexión de nube o puerta de enlace compatible, según configuración. Deben resolverse credenciales y confianza SSL en el entorno que ejecuta la actualización; cambiar de Excel a PostgreSQL no corrige automáticamente el certificado.
6. Railway debe estar encendido y con crédito disponible. No se han cambiado sus certificados ni desactivado TLS en los archivos entregados.

Para demostrar una actualización sin alterar controles, trabaja con una copia del libro: cambia un nombre de sucursal, actualiza el informe, comprueba el nuevo nombre y restaura la copia. No cambies los archivos maestros durante el ejercicio de comparación de fuentes.

## Documentación oficial consultada

- Modelo estrella: https://learn.microsoft.com/en-us/power-bi/guidance/star-schema/
- Calendario: https://learn.microsoft.com/en-us/power-bi/guidance/model-date-tables
- Conector PostgreSQL: https://learn.microsoft.com/en-us/power-query/connectors/postgresql
- Actualización y gateway: https://learn.microsoft.com/en-us/power-bi/connect-data/service-gateway-enterprise-manage-scheduled-refresh
- Pronóstico: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-analytics-pane
- Influenciadores clave: https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-influencers
- Railway PostgreSQL: https://docs.railway.com/databases/postgresql

Las fuentes documentan las herramientas. Todos los datos de la empresa fueron generados para este curso.
