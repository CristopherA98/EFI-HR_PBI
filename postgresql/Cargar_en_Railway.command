#!/bin/zsh
set -eu
[[ -f "${0:A:h}/conexion.local" ]] && source "${0:A:h}/conexion.local"
if [[ -z "${RAILWAY_HOST:-}" || -z "${RAILWAY_PORT:-}" ]]; then
    read -r '?Host de Railway (ej. xxxx.proxy.rlwy.net): ' RAILWAY_HOST
    read -r '?Puerto: ' RAILWAY_PORT
fi
BASE_CURSO="${0:A:h}"
if command -v psql >/dev/null 2>&1; then
    CLIENTE_PSQL="$(command -v psql)"
elif [[ -x /opt/homebrew/opt/postgresql@16/bin/psql ]]; then
    CLIENTE_PSQL=/opt/homebrew/opt/postgresql@16/bin/psql
else
    echo 'No se encontró psql. Usa DBeaver o pgAdmin para ejecutar 01_crear_condor_curso.sql.'
    exit 1
fi
echo 'Se creará condor_curso en Railway. Se conservan condor y public.'
echo 'Si condor_curso ya existe, se detendrá sin borrar sus tablas.'
printf 'Contraseña de PostgreSQL (no se ve al escribir; puedes pegarla con Cmd+V): '; read -rs PGPASSWORD; echo
if [[ -z "$PGPASSWORD" ]]; then echo 'No escribiste contraseña. Vuelve a ejecutar el archivo.'; read -r '?Enter para cerrar.'; exit 1; fi
export PGPASSWORD
"$CLIENTE_PSQL" "host=$RAILWAY_HOST port=$RAILWAY_PORT dbname=railway user=postgres sslmode=require connect_timeout=15" -w -v ON_ERROR_STOP=1 -f "$BASE_CURSO/01_crear_condor_curso.sql"
echo 'Carga terminada. Selecciona el esquema condor_curso en Power BI.'
read -r '?Presiona Enter para cerrar.'
