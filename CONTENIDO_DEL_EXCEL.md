# Farmacias Cóndor: qué contiene el Excel

Archivo: `Farmacias_Condor_Curso.xlsx`. Base sintética, ene 2023 – ago 2026: 900 personas, 27 centros, 6 áreas, 16 cargos.

## 1. Pregunta de negocio

**¿En qué cargos y sucursales de operación de farmacia perdemos más gente y cuánto cuesta reemplazarla?**

| Eslabón | Definición |
|---|---|
| Objetivo | Farmacias atendidas con personal estable y capacitado |
| OKR | Reducir la rotación de la primera línea de farmacia |
| Resultado clave | Rotación anualizada de Auxiliares y Cajeros de 35–44 % a menos de 25 % en 12 meses |
| KPI | Rotación, costo por contratación, días de cobertura, índice de ausentismo |
| Umbral | Rotación mensual > 3 % = alerta. Responsable: Operaciones con Talento Humano |

Detalle en `materiales/PREGUNTA_DE_NEGOCIO.md`.

## 2. Tablas del modelo

| Hoja | Filas | Qué contiene | Uso |
|---|---:|---|---|
| fact_plantilla | 18.961 | Una fila por persona y mes (headcount, horas, sueldo) | Denominador de rotación |
| fact_movimientos | 967 | Ingresos y salidas con motivo | Dónde se pierde gente |
| fact_contrataciones | 550 | Procesos cubiertos, fuente y costos | Costo y días de cobertura |
| fact_ausencias | 14.572 | Ausencias de 4 u 8 horas | Índice de ausentismo |
| fact_capacitacion | 3.565 | Participaciones en cursos, horas, nota | Opcional |
| dim_colaborador | 900 | Datos personales, fechas de ingreso y salida | Antigüedad al salir |
| dim_cargo | 16 | Cargo, nivel, familia | Corte por cargo |
| dim_sucursal | 27 | Ciudad, provincia, región, tipo de centro | Corte por sucursal y región |
| dim_area | 6 | Área y dirección | Corte por área |
| dim_antiguedad | 4 | Rangos de antigüedad | Salidas tempranas |
| dim_calendario | 1.461 | Fechas 2023–2026 | Tiempo |

Esquema en estrella: cada dimensión filtra a los hechos (uno a muchos, un solo sentido). Los hechos no se relacionan entre sí.

## 3. Hojas de apoyo

| Hoja | Para qué sirve |
|---|---|
| Control_mensual | 44 meses de valores esperados para validar las medidas |
| Diccionario | Tabla, campo, tipo y descripción (121 campos) |
| Relaciones | Las 30 relaciones del modelo |
| Practicas | Ejercicios del curso |
| Inicio | Índice del libro |

## 4. Tablas raw (con problemas a propósito)

Sirven para practicar Power Query. **No las cargues junto con las limpias**: duplicarías datos.

### raw_colaboradores (912 filas, debe quedar en 900)

| Problema | Cantidad | Solución |
|---|---:|---|
| Filas duplicadas exactas | 12 | Quitar duplicados |
| Espacios sobrantes en apellidos | 30 | Recortar y limpiar |
| Género vacío o en minúsculas | 18 vacíos | Normalizar; vacío = "No informado" |
| Fecha de ingreso como texto dd/MM/yyyy | 20 | Convertir con `fxFechaMixta` |
| Fecha de salida vacía | 483 | **Conservar**: son personas activas |

### raw_plantilla (761 filas, debe quedar en 751)

Muestra de enero y febrero de 2023. No reemplaza a `fact_plantilla`.

| Problema | Cantidad | Solución |
|---|---:|---|
| Filas duplicadas | 10 | Quitar duplicados |
| Sueldo como texto con coma decimal | 25 | Convertir con cultura es-EC |
| Fecha como texto dd/MM/yyyy | 15 | Convertir con `fxFechaMixta` |
| `activo_cierre = 0` | varias | **Conservar**: son salidas del mes |

Las funciones M están en `materiales/POWER_QUERY.txt`.

## 5. Valores de control (agosto 2026)

| Medida | Valor |
|---|---|
| Headcount | 486 al inicio, 483 al cierre |
| Ingresos / salidas | 11 / 14 |
| Rotación | 2,89 % |
| Ausentismo | 3,09 % |
| Costo por contratación | USD 162,09 |

## 6. Otras fuentes de los mismos datos

`csv/` (una tabla por archivo, UTF-8), `postgresql/` (esquema `condor_curso`) y `movimientos_por_anio/` (967 movimientos en cuatro archivos). Usa una sola fuente por tabla.
