# Farmacias Cóndor: construcción del dashboard en Power BI Desktop

Edición Curso 20260925. Esta guía convierte el modelo en un informe de tres páginas y sirve de plantilla para construir el .pbix de referencia. Las medidas están en `MEDIDAS_DAX.txt`; aquí solo se indica dónde usarlas. Cifras de control: agosto 2026 (ver al final).

## 0. Preparación (15 min)

1. Carga las 11 tablas `dim_*` y `fact_*` (Excel, CSV o PostgreSQL `condor_curso`). No cargues las hojas raw ni Control_mensual junto a las limpias.
2. Crea las 30 relaciones de la hoja Relaciones (uno a muchos, filtro dimensión → hecho). Oculta las claves en la vista de informe.
3. Marca `dim_calendario` como tabla de fechas (columna `fecha`). Ordena `mes_nombre` por `mes`.
4. Crea las columnas calculadas y todas las medidas de `MEDIDAS_DAX.txt`. Guárdalas en una tabla vacía `_Medidas` para tenerlas juntas.
5. Comprueba primero: matriz por `anio_mes` con Headcount inicio, Ingresos, Salidas, Headcount cierre y Balance plantilla (debe ser 0 en todos los meses). Contrasta con la hoja Control_mensual antes de dibujar nada.
6. Filtro de página/informe: `dim_calendario[inicio_mes]` entre 01/01/2023 y 01/08/2026.

## 1. Estilo común

- Lienzo 16:9. Fondo claro, una sola paleta: un color principal para la métrica en foco y gris para el contexto. Rojo solo para alertas.
- Título en cada visual con el periodo analizado (ej.: "Rotación mensual, ene 2023 – ago 2026").
- Etiquetas de datos en lugar de depender solo del color. Formatos: rotación e índice de ausentismo con 1 decimal en %, costos en USD sin decimales, `Rotacion diferencia pp` como número.
- Segmentadores sincronizados en las tres páginas (Vista → Sincronizar segmentadores): año-mes, área, cargo, género, tramo de antigüedad y región.
- Activa Editar interacciones donde un visual no deba filtrar a otro (ver página 3).

## 2. Página 1: Resumen ejecutivo

| Visual | Campos | Nota |
|---|---|---|
| Tarjeta | Headcount cierre | Formato entero |
| Tarjeta | Rotacion | % con 1 decimal |
| Tarjeta | Indice ausentismo | % con 1 decimal |
| Tarjeta | Costo por contratacion | USD |
| Líneas | Eje: `dim_calendario[inicio_mes]` (jerarquía continua); valores: Headcount cierre | Una serie, sin leyenda |
| Barras horizontales | Eje: `dim_area[area]`; valores: Salidas | Ordenar descendente |
| Tarjeta KPI o texto | Variacion headcount anual, Rotacion diferencia pp | Con la advertencia de 2026 parcial |

Mensaje sugerido para el título de página: "En agosto 2026 la plantilla baja de 486 a 483: 11 ingresos, 14 salidas."

## 3. Página 2: Operación y ausentismo

1. Matriz: filas `dim_sucursal` (jerarquía región → provincia → ciudad → sucursal); valores: Headcount cierre, Horas programadas, Horas ausencia, Indice ausentismo. Formato condicional de datos en el índice.
2. Barras: sucursal vs Indice ausentismo, ordenado, con Horas programadas en la información sobre herramientas. Una tasa sin denominador engaña.
3. Columnas agrupadas: Indice ausentismo por `dim_antiguedad`.
4. Mapa (opcional): categoriza latitud/longitud como coordenadas; son centros de ciudad aproximados.
5. Tooltip personalizado (página oculta con Headcount cierre y Horas programadas) para todos los visuales de tasas.

## 4. Página 3: Atracción y desarrollo

1. Barras: Costo por contratacion por fuente/canal de reclutamiento; segunda serie o tooltip con Contrataciones.
2. Barras: Dias cobertura promedio por cargo (destaca Químico Farmacéutico u otros cargos de cobertura larga).
3. Columnas: Horas capacitacion y Personas capacitadas por área; tarjeta con Nota promedio (los pendientes son nulos, no cero).
4. Drill-through: página de detalle del proceso de contratación (id, cargo, sucursal, costos, días de cobertura).
5. Editar interacciones: el segmentador de fuente/canal no debe filtrar los visuales de plantilla (solo existe en contrataciones).

## 5. Pronóstico (ejercicio aparte, 20 min)

1. Nueva página con línea de Costo personal simulado (o Headcount cierre) por mes, una sola serie.
2. Panel Analítica → Pronóstico: 6 meses, intervalo de confianza 95 %, estacionalidad automática o 12.
3. Prueba temporal: reserva mar–ago 2026. Configura el pronóstico con "Ignorar último" = 6 puntos y compara con lo real.
4. MAE = promedio de ABS(real − pronóstico). Referencia ingenua: repetir el último valor de febrero 2026. Si el pronóstico no gana a la referencia, dilo: es un resultado válido.
5. Recordar: 44 meses de datos sintéticos enseñan la técnica, no validan una política real.

## 6. IA descriptiva (opcional)

Influenciadores clave en una copia de `fact_plantilla` enriquecida con cargo y región, analizando `horas_extra`. No uses `costo_extra` como explicador (deriva de `horas_extra`). No conectes la copia al modelo principal. Asociación no es causalidad.

## 7. Publicación

1. Guardar `Farmacias_Condor_Curso.pbix`. Publicar en un espacio de trabajo autorizado.
2. Configurar credenciales del modelo semántico; probar "Actualizar ahora" antes de programar.
3. Excel/CSV locales exigen puerta de enlace; PostgreSQL en Railway exige resolver SSL/credenciales en el entorno que actualiza. Railway debe estar encendido y con crédito.

## 8. Lista de comprobación final

- [ ] Agosto 2026: Headcount inicio 486, ingresos 11, salidas 14, cierre 483, promedio 484,5.
- [ ] Rotación 2,89 %, ausentismo 3,09 % (86.112 h programadas, 2.660 h ausentes).
- [ ] 11 contrataciones, costo USD 1.783,03, costo por contratación USD 162,09.
- [ ] Costo de personal simulado USD 511.116,36.
- [ ] Balance plantilla = 0 en los 44 meses.
- [ ] fact_plantilla conserva 18.961 filas tras cualquier combinación; movimientos suman 967.
- [ ] Ningún visual suma headcount de varios meses ni promedia porcentajes.
- [ ] Todos los títulos muestran el periodo; 2026 no se compara contra 2025 completo sin aclararlo.

## 9. Después de construirlo

Guarda el .pbix en esta carpeta y, si quieres una plantilla para los participantes, expórtalo también como `.pbit` (Archivo → Exportar → Plantilla de Power BI), sin datos.
