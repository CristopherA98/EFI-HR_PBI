#!/bin/zsh
set -eu
[[ -f "${0:A:h}/conexion.local" ]] && source "${0:A:h}/conexion.local"
if [[ -z "${RAILWAY_HOST:-}" || -z "${RAILWAY_PORT:-}" ]]; then
    read -r '?Host de Railway (ej. xxxx.proxy.rlwy.net): ' RAILWAY_HOST
    read -r '?Puerto: ' RAILWAY_PORT
fi
if command -v psql >/dev/null 2>&1; then
    PSQL="$(command -v psql)"
elif [[ -x /opt/homebrew/opt/postgresql@16/bin/psql ]]; then
    PSQL=/opt/homebrew/opt/postgresql@16/bin/psql
else
    echo 'No se encontró psql. Usa DBeaver o pgAdmin y ejecuta: DROP SCHEMA condor CASCADE;'
    exit 1
fi
CONN="host=$RAILWAY_HOST port=$RAILWAY_PORT dbname=railway user=postgres sslmode=require connect_timeout=15"

echo 'Este script BORRA el esquema "condor" (edición inicial, 600 personas) en Railway.'
echo 'NO toca "condor_curso" ni "public".'
echo 'Introduce la contraseña de PostgreSQL (no se muestra ni se guarda).'
printf 'Contraseña: '; read -rs PGPASSWORD; echo; export PGPASSWORD

echo; echo '--- Estado actual ---'
"$PSQL" "$CONN" -v ON_ERROR_STOP=1 -c "SELECT table_schema AS esquema, count(*) AS tablas FROM information_schema.tables WHERE table_schema IN ('condor','condor_curso') GROUP BY 1 ORDER BY 1;"

echo; echo '--- Comprobando que condor_curso esté completo ---'
N=$("$PSQL" "$CONN" -At -v ON_ERROR_STOP=1 -c "SELECT (SELECT count(*) FROM condor_curso.dim_colaborador)||'|'||(SELECT count(*) FROM condor_curso.fact_plantilla);")
echo "dim_colaborador | fact_plantilla = $N  (esperado 900|18961)"
if [[ "$N" != "900|18961" ]]; then
    echo 'condor_curso no está completo. No se borra nada.'
    read -r '?Presiona Enter para cerrar.'; exit 1
fi

echo
read -r '?Escribe BORRAR para eliminar el esquema condor (o Enter para cancelar): ' R
if [[ "$R" != "BORRAR" ]]; then echo 'Cancelado. No se cambió nada.'; read -r '?Enter para cerrar.'; exit 0; fi

"$PSQL" "$CONN" -v ON_ERROR_STOP=1 -c "DROP SCHEMA IF EXISTS condor CASCADE;"
echo; echo '--- Resultado ---'
"$PSQL" "$CONN" -v ON_ERROR_STOP=1 -c "SELECT table_schema AS esquema, count(*) AS tablas FROM information_schema.tables WHERE table_schema IN ('condor','condor_curso') GROUP BY 1 ORDER BY 1;"
echo 'Listo. Solo queda condor_curso.'
read -r '?Presiona Enter para cerrar.'
