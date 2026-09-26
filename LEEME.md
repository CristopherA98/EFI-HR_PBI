# Farmacias Cóndor — paquete del curso

Empieza con **Farmacias_Condor_Curso.xlsx**. Puedes practicar sin Railway ni DuckDB.

## Contenido

- **Farmacias_Condor_Curso.xlsx**: base limpia en 11 tablas, dos fuentes con errores deliberados, diccionario completo, relaciones, ejercicios y controles mensuales.
- **csv/**: exactamente los mismos registros en CSV UTF-8. Incluye particiones anuales de movimientos para combinar archivos.
- **postgresql/01_crear_condor_curso.sql**: crea y carga las mismas 13 tablas, incluidas las dos raw. Tiene claves primarias, foráneas y restricciones. No borra datos existentes.
- **postgresql/02_verificar.sql**: consulta de conteos e indicadores mensuales.
- **materiales/GUIA_DEL_CURSO.md**: secuencia de prácticas, definiciones de indicadores, dashboard, pronóstico y publicación.
- **materiales/MEDIDAS_DAX.txt**: calendario, columnas y medidas listas para copiar una a una.
- **materiales/POWER_QUERY.txt**: limpieza y combinación de datos en M.
- **materiales/GUIA_DASHBOARD_PASO_A_PASO.md**: construcción del dashboard de tres páginas, pronóstico, publicación y lista de comprobación.

## Edición y alcance

900 personas históricas; 483 activas al 31/08/2026; 27 centros; 6 áreas; 16 cargos. Enero de 2023–agosto de 2026: 44 meses. Dim_calendario cubre 2023–2026 completos. Datos y costos íntegramente sintéticos, en USD. No constituyen cálculo legal de nómina.

Esta edición del curso es más completa que la base inicial de 600 personas. Se carga en **condor_curso** y conserva las tablas anteriores de **condor**. No mezcles ambas ediciones al comprobar indicadores.

## Cargar en Railway, sin instalar programas nuevos en tu Mac

El cliente psql ya está disponible en tu Mac, porque lo usaste para cargar la primera base.

1. Abre la carpeta postgresql.
2. Ejecuta **Cargar_en_Railway.command**. Si macOS no lo abre, abre Terminal, escribe `zsh ` y arrastra el archivo a Terminal; presiona Enter.
3. Introduce la contraseña de Railway. No se muestra al escribir y no se guarda en el script.
4. Espera a los conteos finales. No ejecutes la carga de nuevo si ya finalizó: por diseño se detiene si el esquema existe.
5. En Power BI elige las tablas de **condor_curso**.

Los scripts leen host y puerto de postgresql/conexion.local (no se sube a GitHub) o los piden al ejecutarse: `TU_HOST.proxy.rlwy.net:TU_PUERTO`, base `railway`, usuario `postgres`. Si cambiaron, edita ese archivo o utiliza tu cliente PostgreSQL habitual. El SSL de Power BI debe resolverse aparte; Excel permite continuar el curso mientras tanto.

Alternativa: abre 01_crear_condor_curso.sql en DBeaver/pgAdmin y ejecuta el script completo. No contiene comandos exclusivos de psql.

## Estado de entrega

La base se creó y validó en PostgreSQL local y se cargó en Railway (esquema condor_curso). La base antigua que ya cargaste sigue siendo otra edición.

No se entrega un PBIX ni se ha publicado un reporte. El material permite construirlos durante el curso. Revisa materiales/VERIFICACION.md para las comprobaciones de los archivos.
