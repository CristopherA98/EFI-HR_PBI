COPY condor_curso.dim_area TO '/Users/caguirre/Library/CloudStorage/OneDrive-Personal/Capacitaciones/EFI_Cordillera/People_Analytics_PBI/outputs/condor_curso_20260925/soporte/pg_export/dim_area.csv' WITH (FORMAT CSV, HEADER TRUE);
COPY condor_curso.dim_cargo TO '/Users/caguirre/Library/CloudStorage/OneDrive-Personal/Capacitaciones/EFI_Cordillera/People_Analytics_PBI/outputs/condor_curso_20260925/soporte/pg_export/dim_cargo.csv' WITH (FORMAT CSV, HEADER TRUE);
COPY condor_curso.dim_sucursal TO '/Users/caguirre/Library/CloudStorage/OneDrive-Personal/Capacitaciones/EFI_Cordillera/People_Analytics_PBI/outputs/condor_curso_20260925/soporte/pg_export/dim_sucursal.csv' WITH (FORMAT CSV, HEADER TRUE);
COPY condor_curso.dim_antiguedad TO '/Users/caguirre/Library/CloudStorage/OneDrive-Personal/Capacitaciones/EFI_Cordillera/People_Analytics_PBI/outputs/condor_curso_20260925/soporte/pg_export/dim_antiguedad.csv' WITH (FORMAT CSV, HEADER TRUE);
COPY condor_curso.dim_calendario TO '/Users/caguirre/Library/CloudStorage/OneDrive-Personal/Capacitaciones/EFI_Cordillera/People_Analytics_PBI/outputs/condor_curso_20260925/soporte/pg_export/dim_calendario.csv' WITH (FORMAT CSV, HEADER TRUE);
COPY condor_curso.dim_colaborador TO '/Users/caguirre/Library/CloudStorage/OneDrive-Personal/Capacitaciones/EFI_Cordillera/People_Analytics_PBI/outputs/condor_curso_20260925/soporte/pg_export/dim_colaborador.csv' WITH (FORMAT CSV, HEADER TRUE);
COPY condor_curso.fact_plantilla TO '/Users/caguirre/Library/CloudStorage/OneDrive-Personal/Capacitaciones/EFI_Cordillera/People_Analytics_PBI/outputs/condor_curso_20260925/soporte/pg_export/fact_plantilla.csv' WITH (FORMAT CSV, HEADER TRUE);
COPY condor_curso.fact_movimientos TO '/Users/caguirre/Library/CloudStorage/OneDrive-Personal/Capacitaciones/EFI_Cordillera/People_Analytics_PBI/outputs/condor_curso_20260925/soporte/pg_export/fact_movimientos.csv' WITH (FORMAT CSV, HEADER TRUE);
COPY condor_curso.fact_ausencias TO '/Users/caguirre/Library/CloudStorage/OneDrive-Personal/Capacitaciones/EFI_Cordillera/People_Analytics_PBI/outputs/condor_curso_20260925/soporte/pg_export/fact_ausencias.csv' WITH (FORMAT CSV, HEADER TRUE);
COPY condor_curso.fact_contrataciones TO '/Users/caguirre/Library/CloudStorage/OneDrive-Personal/Capacitaciones/EFI_Cordillera/People_Analytics_PBI/outputs/condor_curso_20260925/soporte/pg_export/fact_contrataciones.csv' WITH (FORMAT CSV, HEADER TRUE);
COPY condor_curso.fact_capacitacion TO '/Users/caguirre/Library/CloudStorage/OneDrive-Personal/Capacitaciones/EFI_Cordillera/People_Analytics_PBI/outputs/condor_curso_20260925/soporte/pg_export/fact_capacitacion.csv' WITH (FORMAT CSV, HEADER TRUE);
COPY condor_curso.raw_colaboradores TO '/Users/caguirre/Library/CloudStorage/OneDrive-Personal/Capacitaciones/EFI_Cordillera/People_Analytics_PBI/outputs/condor_curso_20260925/soporte/pg_export/raw_colaboradores.csv' WITH (FORMAT CSV, HEADER TRUE);
COPY condor_curso.raw_plantilla TO '/Users/caguirre/Library/CloudStorage/OneDrive-Personal/Capacitaciones/EFI_Cordillera/People_Analytics_PBI/outputs/condor_curso_20260925/soporte/pg_export/raw_plantilla.csv' WITH (FORMAT CSV, HEADER TRUE);
COPY (WITH p AS (SELECT fecha, sum(activo_inicio) AS hc_inicio, sum(activo_cierre) AS hc_cierre,
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
ORDER BY fecha) TO '/Users/caguirre/Library/CloudStorage/OneDrive-Personal/Capacitaciones/EFI_Cordillera/People_Analytics_PBI/outputs/condor_curso_20260925/soporte/pg_export/controles.csv' WITH (FORMAT CSV, HEADER TRUE);
