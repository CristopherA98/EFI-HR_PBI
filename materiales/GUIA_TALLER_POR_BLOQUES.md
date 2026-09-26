# Guía del taller: People Analytics con Power BI

Caso integrador: **Farmacias Cóndor** (datos sintéticos, enero 2023 – agosto 2026). Esta guía ordena el taller en tres bloques, según el temario acordado. Para el detalle de cada práctica se remite a `GUIA_DEL_CURSO.md`, `MEDIDAS_DAX.txt`, `POWER_QUERY.txt` y `GUIA_DASHBOARD_PASO_A_PASO.md`.

**Duración propuesta (8 horas académicas, ajustable):** Bloque 1 ≈ 3 h · Bloque 2 ≈ 2,5 h · Bloque 3 ≈ 2,5 h. Los tiempos son una propuesta; ensaya la unidad de DAX, que suele ser la más apretada.

**Materiales del alumno:** `Farmacias_Condor_Curso.xlsx` (empieza por aquí), carpeta `csv/` y, opcionalmente, el esquema `condor_curso` en PostgreSQL. Nadie necesita Railway para seguir el curso.

## ¿Hay datos sucios para practicar transformaciones? Sí

Las dos fuentes **raw** traen errores deliberados. Las tablas limpias equivalentes sirven de solución para comprobar el resultado.

| Fuente | Problema | Cantidad | Herramienta de Power Query |
|---|---|---:|---|
| raw_colaboradores | Filas duplicadas exactas (912 entrada → 900 personas) | 12 | Quitar duplicados |
| raw_colaboradores | Espacios al inicio y al final en `apellidos` (ej. `"  Torres Molina  "`) | 30 | Transformar → Recortar / Limpiar |
| raw_colaboradores | `genero` con mayúsculas inconsistentes (`femenino`, `masculino`) | 29 | Reemplazar valores / Poner en mayúsculas cada palabra |
| raw_colaboradores | `genero` vacío (falta de información) | 18 | Reemplazar nulos por `No informado` |
| raw_colaboradores | `fecha_ingreso` como texto `dd/MM/yyyy` (ej. `13/12/2018`) mezclada con fechas ISO | 20 | Cambiar tipo usando configuración regional / columna condicional |
| raw_colaboradores | `fecha_salida` vacía: **no es un error**, significa persona activa | 483 activas | Conservar el nulo |
| raw_plantilla | Filas duplicadas exactas (761 entrada → 751) | 10 | Quitar duplicados |
| raw_plantilla | `sueldo_mensual` como texto con coma decimal (ej. `"612,73"`) | 25 | Reemplazar `,` por `.` o cambiar tipo con configuración regional es-EC |
| raw_plantilla | `fecha` como texto `dd/MM/yyyy` | 15 | Cambiar tipo usando configuración regional |

Otros nulos con significado que sirven para hablar de valores nulos: notas de capacitación pendientes (no equivalen a cero) y `costo_agencia = 0` en contrataciones sin agencia (cero real, no dato faltante).

Regla didáctica: **cada limpieza se comprueba contra la tabla limpia** (900 filas, 751 filas, mismos valores). Los datos son ficticios; en un caso real, investiga las diferencias antes de deduplicar solo por identificador.

---

# Bloque 1: Datos y modelo (≈ 3 h)

## 1.1 Introducción a Power BI Desktop (20 min)

- **Objetivo:** que el alumno se ubique en la interfaz y entienda el flujo completo antes de tocar datos.
- **Demostración:** las cuatro vistas (Informe, Tabla, Modelo, Consultas DAX), los paneles Campos, Visualizaciones y Filtros, y la cinta Inicio / Transformar / Modelado.
- **Flujo de trabajo para dibujar en la pizarra:** Obtener datos → Transformar (Power Query) → Modelar (relaciones) → Medidas (DAX) → Visualizar → Publicar.
- **Ajustes previos:** desactivar fecha/hora automática y nombrar el archivo `Farmacias_Condor.pbix`.
- **Práctica:** abrir un libro vacío, guardar, reconocer cada panel.

## 1.2 Conexión a fuentes de datos: Excel, CSV y bases de datos (40 min)

- **Excel:** Obtener datos → Libro de Excel → seleccionar solo las tablas `dim_*` y `fact_*`. No cargar las hojas raw junto a las limpias.
- **CSV:** conectar `dim_sucursal.csv` y comprobar que tiene las mismas 27 filas. Carpeta `csv/movimientos_por_anio` con el conector **Carpeta** para combinar 4 archivos: deben resultar 967 movimientos.
- **Base de datos:** PostgreSQL, servidor y base `railway`, esquema `condor_curso`. Modo Importar. El certificado SSL puede dar problemas; si ocurre, seguir con Excel y explicarlo como caso real de TI.
- **Punto de discusión:** ¿cuándo elegir cada origen? (facilidad, actualización, volumen, seguridad).
- **Error a evitar:** anexar Excel y PostgreSQL con los mismos registros: duplica los indicadores.
- **Práctica corta:** traer `dim_sucursal` desde las tres fuentes y comparar.

## 1.3 Power Query: limpieza y combinación (75 min)

Trabaja sobre las tablas raw con la tabla de defectos de arriba, en este orden:

1. **Tipos de datos:** definir Entero, Decimal y Fecha. Explicar por qué un texto con coma decimal rompe las sumas.
2. **Valores nulos:** distinguir un nulo que es error (género vacío) de uno que es información (fecha de salida vacía).
3. **Duplicados:** quitar duplicados exactos y verificar el conteo (900 y 751).
4. **Columnas calculadas:** `Nombre completo` en Power Query (`[nombres] & " " & [apellidos]`), columna condicional de tramo o estado.
5. **Combinación de tablas:** *Combinar consultas* (unión izquierda `fact_plantilla` con `dim_cargo`; deben seguir 18.961 filas) y *Anexar consultas* (movimientos por año).
6. **Agrupar antes de combinar:** resumir `fact_ausencias` por persona y mes antes de unirla a plantilla, o se multiplica la nómina.
7. **Pasos aplicados:** enseñar que Power Query guarda la receta; documentar y renombrar pasos.

- **Entregable:** consulta `colaboradores_limpio` con 900 filas, idéntica a `dim_colaborador`.
- **Comprobación rápida:** `raw_plantilla` limpio debe dar 751 filas y suma de sueldos numérica.

## 1.4 Buenas prácticas de estructura de datos para Talento Humano (20 min)

- **Grano explícito:** una fila = una persona-mes (plantilla), un evento (movimientos, ausencias), una participación (capacitación).
- **Un identificador estable** por persona; sin nombres como llave.
- **Fechas reales** y en un solo formato; **estados y categorías** con lista cerrada.
- **Separar** atributos que cambian poco (dimensiones) de hechos que se repiten.
- **Mínimo dato personal necesario:** para reportes gerenciales no se publican nombres ni datos sensibles; conviene seudonimizar y limitar el acceso. Referencia: material de la LOPDP en `docs/`. Esta guía no es asesoría legal.
- **Definiciones escritas** de cada indicador (diccionario de datos) antes de construirlo.

## 1.5 Modelado: esquema estrella (30 min)

- Cinco tablas de hechos (`fact_plantilla`, `fact_movimientos`, `fact_ausencias`, `fact_contrataciones`, `fact_capacitacion`) y seis dimensiones (calendario, colaborador, área, cargo, sucursal, antigüedad).
- Relaciones uno a muchos, filtro en un solo sentido, de la dimensión al hecho. **No relacionar hechos entre sí.**
- Ocultar las claves en la vista de informe.
- **Ejercicio de diagnóstico:** mostrar el mismo modelo mal armado (todo en una tabla plana) y pedir que expliquen qué se duplica.

## 1.6 Tabla calendario y relaciones (25 min)

- Importar `dim_calendario` o crearla con DAX (`CALENDAR`), **nunca ambas**.
- Marcar como tabla de fechas, ordenar `mes_nombre` por `mes`.
- Relacionar `dim_calendario[fecha]` con la fecha de cada hecho (plantilla el día 1 de cada mes).
- **Prueba de humo del bloque:** matriz por `anio_mes` con conteo de filas de plantilla; deben aparecer 44 meses sin huecos.

**Cierre del bloque:** cada alumno entrega un modelo con las 11 tablas, 30 relaciones y calendario marcado.

---

# Bloque 2: DAX y métricas de Talento Humano (≈ 2,5 h)

## 2.1 Introducción a DAX (20 min)

- **Columna calculada:** se evalúa fila por fila al procesar el modelo (ej. `Dias cobertura`, `Costo proceso`).
- **Medida:** responde al contexto del visual y se calcula al mostrarlo.
- **Demostración:** el mismo `Costo por contratacion` en una tarjeta global, por área y por fuente de reclutamiento.
- Crear una tabla `_Medidas` para organizar.

## 2.2 Funciones esenciales (35 min)

- **Agregación:** `SUM`, `AVERAGE`, `MIN`, `MAX`. **Conteo:** `COUNTROWS`, `DISTINCTCOUNT`.
- **`CALCULATE`** para cambiar el filtro (ej. `Salidas`, `Ingresos` filtrando `tipo_movimiento`).
- **Contexto de filtro vs contexto de fila;** `FILTER`, `VALUES`, `REMOVEFILTERS`, `DIVIDE` y `COALESCE`.
- **Advertencia central:** `DISTINCTCOUNT` de colaboradores en `dim_colaborador` cuenta 900 históricos, **no** el headcount.

## 2.3 Medidas de headcount, ingresos, salidas y rotación mensual (30 min)

- `Headcount inicio`, `Ingresos`, `Salidas`, `Headcount cierre`, `Headcount promedio mensual`, `Rotacion`.
- **Balance de control:** `Balance plantilla = inicio + ingresos − salidas − cierre` debe ser 0 los 44 meses.
- **Stock vs flujo:** el headcount no se suma entre meses; ingresos y salidas sí.
- **Control agosto 2026:** 486 / 11 / 14 / 483; promedio 484,5; rotación 2,89 %.

## 2.4 Tasa de rotación, índice de ausentismo y costo por contratación (30 min)

- **Rotación:** salidas / promedio de plantilla. En varios meses: salidas del periodo / promedio de los headcounts medios mensuales. No sumar porcentajes.
- **Ausentismo:** `Horas ausencia / Horas programadas` (agosto 2026: 3,09 %; 2.660 de 86.112 h).
- **Costo por contratación:** costo total de procesos cubiertos / número de contrataciones (agosto 2026: USD 162,09). No promediar promedios.

## 2.5 Inteligencia de tiempo (25 min)

- `DATEADD` (mes anterior), `SAMEPERIODLASTYEAR` (año anterior), `DATESYTD` (acumulado del año).
- Variaciones mensual y anual del headcount; ingresos y salidas acumulados; costo acumulado.
- **Cuidado:** 2026 solo llega a agosto; no compararlo contra 2025 completo sin aclararlo.
- **Regla:** no acumular headcount (es un stock).

## 2.6 Segmentación (10 min de teoría, resto en práctica)

- Áreas, cargos, género, tramo de antigüedad y ubicación (región → provincia → ciudad → sucursal) con segmentadores y jerarquías.
- `Participacion headcount area` con `REMOVEFILTERS(dim_area)`.
- **Límite:** el balance por antigüedad no cierra en periodos largos porque las personas cambian de tramo; para conciliar usar total, área, cargo, género o ubicación.

**Cierre del bloque:** una matriz por mes con las medidas clave contrastada con la hoja `Control_mensual` del Excel.

---

# Bloque 3: Visualización, storytelling y publicación (≈ 2,5 h)

## 3.1 Principios de visualización efectiva (20 min)

| Pregunta | Gráfico recomendado |
|---|---|
| ¿Cómo cambia en el tiempo? | Líneas (una serie por eje mensual continuo) |
| ¿Cómo se comparan categorías? | Barras horizontales ordenadas |
| ¿Cuánto pesa cada parte? | Barras 100 % o tarjeta; evitar tortas de más de 3 partes |
| ¿Cómo se relacionan dos medidas? | Dispersión |
| ¿Cifra clave? | Tarjeta con meta o variación |

Regla: un color de énfasis y gris para el contexto; rojo solo para alerta; etiquetas de datos en lugar de depender del color.

## 3.2 Errores frecuentes en la reportería de Talento Humano (15 min)

- Sumar el headcount de varios meses.
- Usar los 900 históricos como si fueran activos.
- Calcular rotación sobre ingresados.
- Mezclar días calendario con horas de ausencia.
- Unir hechos sin agrupar (multiplica filas).
- Promediar porcentajes.
- Comparar 2026 parcial con 2025 completo.
- Mostrar una tasa sin su denominador (una sucursal pequeña con 1 salida parece crítica).
- Gráficos de torta con muchas categorías, ejes truncados, colores sin etiqueta.

## 3.3 Diseño y construcción del dashboard ejecutivo (45 min)

Se construye en tres páginas (detalle en `GUIA_DASHBOARD_PASO_A_PASO.md`): **Resumen ejecutivo**, **Operación y ausentismo**, **Atracción y desarrollo**. Se construye por capas: lienzo y título → tarjetas → tendencia → comparativo por área → segmentadores → formato final. Como inspiración, usa el boceto de diseño "Boceto dashboard Farmacias Cóndor" (lienzo publicado en Claude, no es un archivo del repositorio): muestra las tres páginas terminadas y cuatro pasos de construcción. Las cifras del boceto salen de `soporte/boceto_datos.json`.

## 3.4 Interactividad (25 min)

- **Segmentadores** sincronizados entre páginas.
- **Filtros** por visual, página e informe.
- **Drill-down** en la jerarquía región → provincia → ciudad → sucursal.
- **Tooltips** personalizados con headcount y horas programadas.
- **Drill-through** al detalle de un proceso de contratación.
- **Editar interacciones:** decidir qué visual no debe filtrar a otro.

## 3.5 Storytelling con datos para la alta dirección (20 min)

Estructura: **contexto → hallazgo → causa probable → acción → riesgo**. Ejemplo con los datos: en agosto la plantilla baja de 486 a 483 (11 ingresos, 14 salidas). Antes de proponer acciones se segmenta por área y sucursal y se formulan hipótesis. Las diferencias son patrones diseñados en la simulación, no evidencia causal. Un buen título afirma el hallazgo; un mal título describe el gráfico.

## 3.6 Analítica predictiva e inteligencia artificial aplicadas a personas (25 min)

- **Pronóstico agregado:** línea de headcount o costo de personal por mes; panel Analítica → Pronóstico, 6 meses, intervalo de confianza. Prueba temporal: reservar marzo–agosto 2026 y comparar con lo real; MAE contra la referencia ingenua (repetir el último valor).
- **IA descriptiva:** Influenciadores clave sobre `horas_extra` (no usar `costo_extra`, deriva de ella). Asociación no es causalidad.
- **Ética y límites:** no clasificar ni puntuar personas; usar agregados; 44 meses sintéticos enseñan la técnica, no validan una política real. No requiere Copilot ni servicio de pago.

## 3.7 Publicación y actualización en el Servicio de Power BI (20 min)

1. Guardar y **publicar** en un espacio de trabajo autorizado.
2. Configurar credenciales del modelo semántico y ejecutar **Actualizar ahora**.
3. **Actualización programada:** los archivos locales requieren una puerta de enlace; alternativa OneDrive/SharePoint o base en la nube. Confirmar licencia y permisos con TI.
4. Demostrar la actualización con una copia del libro: cambiar un nombre de sucursal, actualizar y comprobar.
5. Compartir con seguridad: nivel de fila si corresponde, y limitar quién ve datos personales.

**Cierre del taller:** proyecto final (dashboard de tres páginas con historia de una página) y autoevaluación con la lista de comprobación final de `GUIA_DASHBOARD_PASO_A_PASO.md`.

---

## Verificación de la guía

- Las cifras (900/912, 751/761, 12, 10, 30, 29, 18, 20, 25, 15, 483 y los controles de agosto 2026) se calcularon sobre los archivos CSV del paquete.
- Los tiempos y el reparto en tres bloques son una propuesta, no medidos en clase.
- Las medidas DAX y consultas M deben ejecutarse en Power BI Desktop para validarse; este paquete no incluye un `.pbix`.
