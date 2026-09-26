-- Comprobaciones de la edición del curso; solo lectura.
SELECT 'dim_colaborador' AS tabla, count(*) AS filas FROM condor_curso.dim_colaborador
UNION ALL SELECT 'fact_plantilla', count(*) FROM condor_curso.fact_plantilla
UNION ALL SELECT 'fact_movimientos', count(*) FROM condor_curso.fact_movimientos
UNION ALL SELECT 'fact_ausencias', count(*) FROM condor_curso.fact_ausencias
UNION ALL SELECT 'fact_contrataciones', count(*) FROM condor_curso.fact_contrataciones
UNION ALL SELECT 'fact_capacitacion', count(*) FROM condor_curso.fact_capacitacion;

-- Headcount, numerador y denominador de rotación mensual.
WITH p AS (
 SELECT fecha, sum(activo_inicio) AS hc_inicio, sum(activo_cierre) AS hc_cierre,
 sum(horas_programadas) AS horas_programadas, sum(pago_base+costo_extra) AS costo_personal
 FROM condor_curso.fact_plantilla GROUP BY fecha
), m AS (
 SELECT date_trunc('month',fecha)::date AS fecha,
 count(*) FILTER (WHERE tipo_movimiento='Ingreso') AS ingresos,
 count(*) FILTER (WHERE tipo_movimiento='Salida') AS salidas
 FROM condor_curso.fact_movimientos GROUP BY 1
), a AS (
 SELECT date_trunc('month',fecha)::date AS fecha, sum(horas_ausencia) AS horas_ausencia
 FROM condor_curso.fact_ausencias GROUP BY 1
), c AS (
 SELECT date_trunc('month',fecha)::date AS fecha, count(*) AS contrataciones,
 sum(costo_publicacion+costo_evaluacion+costo_agencia) AS costo_contratacion
 FROM condor_curso.fact_contrataciones GROUP BY 1
)
SELECT p.fecha, p.hc_inicio, coalesce(m.ingresos,0) AS ingresos,
 coalesce(m.salidas,0) AS salidas, p.hc_cierre,
 (p.hc_inicio+p.hc_cierre)/2.0 AS hc_promedio,
 coalesce(m.salidas,0)/nullif((p.hc_inicio+p.hc_cierre)/2.0,0) AS rotacion,
 p.horas_programadas, coalesce(a.horas_ausencia,0) AS horas_ausencia,
 coalesce(a.horas_ausencia,0)::numeric/nullif(p.horas_programadas,0) AS indice_ausentismo,
 coalesce(c.contrataciones,0) AS contrataciones, coalesce(c.costo_contratacion,0) AS costo_contratacion_total,
 c.costo_contratacion/nullif(c.contrataciones,0) AS costo_por_contratacion,
 p.costo_personal AS costo_personal_simulado
FROM p LEFT JOIN m USING(fecha) LEFT JOIN a USING(fecha) LEFT JOIN c USING(fecha)
ORDER BY fecha;
