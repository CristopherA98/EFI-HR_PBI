# Verificación de la edición Curso 20260925

## Datos

- 900 personas, claves únicas y al menos 18 años cumplidos al ingreso.
- 27 centros, 6 áreas, 16 cargos y 4 tramos de antigüedad.
- Calendario continuo de 1.461 días, del 01/01/2023 al 31/12/2026.
- 18.961 registros de plantilla mensual, 967 movimientos, 14.572 ausencias, 550 contrataciones y 3.565 participaciones en capacitación.
- Todas las claves externas encuentran su dimensión.
- Las ausencias ocurren dentro del vínculo y en turnos programados; su suma no supera las horas programadas de cada persona y mes.
- Plantilla y eventos utilizan el mismo tramo de antigüedad mensual.
- Cada contratación corresponde a un ingreso de los 550 ocurridos dentro del periodo observado.
- El balance inicial + ingresos − salidas = final se cumple en los 44 meses; el headcount se contrastó además con las fechas de ingreso y salida.

## Tres formatos

Excel, CSV y PostgreSQL se generan desde una única colección de datos, con semilla 25092026. Se compararon todos los valores, no solo los conteos. En PostgreSQL/CSV las tablas raw conservan texto; en Excel conservan las mezclas de tipos previstas para la práctica.

El SQL fue ejecutado en PostgreSQL 16.13 local. Se crearon las tablas con sus claves y restricciones y se exportaron nuevamente para contrastar sus registros. El SQL de controles produce los mismos indicadores que Python y las fórmulas del Excel.

Se reabrió el XLSX exportado y se verificaron fechas, valores y controles almacenados. Los 44 resultados mensuales coinciden con tolerancia numérica de 0,000001. Las fechas están tipadas en las tablas limpias y los errores de tipo aparecen únicamente en las fuentes raw. Se revisaron vistas renderizadas de las 18 hojas.

Las reglas propuestas de limpieza recuperan las 900 filas de colaboradores y las 751 filas de la muestra de plantilla, iguales a sus correspondientes datos limpios.

## Límites de esta verificación

- No se cargó esta edición en Railway. El script de carga está preparado para crear condor_curso sin alterar condor ni public.
- No se ejecutó Power BI Desktop ni se generó un PBIX. Las medidas DAX y consultas M son material para ejecutar y contrastar durante la práctica; no se afirma una prueba nativa de DAX/M.
- No se ha configurado ni probado actualización en el Servicio de Power BI, gateway o licenciamiento.
- La prueba local de PostgreSQL no valida el certificado SSL ni la disponibilidad del servicio Railway.
- Las cifras describen una simulación didáctica; no son estadísticas del sector ni estimaciones predictivas sobre personas reales.
