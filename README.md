# EFI-HR_PBI · People Analytics con Power BI

Material del curso **Transformación Digital en Talento Humano: People Analytics y Power BI**.
Caso integrador: **Farmacias Cóndor**, cadena ficticia ecuatoriana. Todos los datos son sintéticos (semilla 25092026) y en USD.

## Contenido

| Carpeta / archivo | Qué es |
|---|---|
| `Farmacias_Condor_Curso.xlsx` | Base del curso: 11 tablas limpias, 2 fuentes raw con errores deliberados, diccionario, relaciones, ejercicios y controles mensuales. **Empieza aquí.** |
| `csv/` | Las mismas tablas en CSV UTF-8 (incluye movimientos por año para practicar combinación de archivos). |
| `postgresql/` | Scripts para crear y verificar el esquema `condor_curso` en PostgreSQL / Railway. |
| `materiales/` | Guía del curso, guía paso a paso del dashboard, medidas DAX, consultas Power Query y verificación. |
| `soporte/` | Scripts que generan y verifican los datos (Python / Node). |

## Alcance de los datos

900 personas históricas, 483 activas al 31/08/2026, 27 centros, 6 áreas, 16 cargos, enero 2023 a agosto 2026 (44 meses).
Control de agosto 2026: headcount inicial 486, ingresos 11, salidas 14, cierre 483; rotación 2,89 %; ausentismo 3,09 %.

## Cómo empezar

1. Descarga `Farmacias_Condor_Curso.xlsx`.
2. Sigue `materiales/GUIA_DEL_CURSO.md` y luego `materiales/GUIA_DASHBOARD_PASO_A_PASO.md`.
3. Opcional: carga la base en PostgreSQL con `postgresql/01_crear_condor_curso.sql`. Los scripts `.command` piden el host y el puerto de tu servicio (o los leen de `postgresql/conexion.local`, que no se sube). Nunca subas contraseñas al repositorio.

## Advertencias

Los datos y costos son didácticos, no estadísticas del sector ni cálculo legal de nómina. No se incluye archivo `.pbix`.
