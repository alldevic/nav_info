#! /usr/bin/env sh

set -o errexit
set -o pipefail

if [[ ${DEBUGPY} == 'TRUE' ]] || [[ ${DEBUGPY} == 'True' ]] || [[ ${DEBUGPY} == '1' ]]; then
    echo >&2 "Starting debug server with debugpy..."
    python3 -m debugpy --listen 0.0.0.0:5678 \
        -m uvicorn nav_info.asgi:application \
            --host 0.0.0.0 \
            --port 8000 \
            --access-log \
            --use-colors \
            --log-level info \
            --lifespan off \
            --reload &
fi

function postgres_ready() {
    python3 <<END
import sys
import psycopg2
from os import environ


def get_env(key, default=None):
    val = environ.get(key, default)
    if val == 'True':
        val = True
    elif val == 'False':
        val = False
    return val

try:
    dbname = get_env('POSTGRES_DB')
    user = get_env('POSTGRES_USER')
    password = get_env('POSTGRES_PASSWORD')
    host = get_env('POSTGRES_HOST')
    port = 5432
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
    echo >&2 "Postgres is unavailable - sleeping"
    sleep 1
done

echo >&2 "Postgres is up - continuing..."

echo >&2 "Migrating..."
python3 manage.py migrate

echo >&2 "Collect static..."
python3 manage.py collectstatic --noinput

if [[ ${DEBUGPY} == 'TRUE' ]] || [[ ${DEBUGPY} == 'True' ]] || [[ ${DEBUGPY} == '1' ]]; then
    wait
elif [[ ${DEBUG} == 'TRUE' ]] || [[ ${DEBUG} == 'True' ]] || [[ ${DEBUG} == '1' ]]; then
    echo >&2 "Starting debug server..."
    exec python3 -m uvicorn nav_info.asgi:application \
            --host 0.0.0.0 \
            --port 8000 \
            --access-log \
            --use-colors \
            --log-level info \
            --lifespan off \
            --reload
else
    echo >&2 "Starting Gunicorn..."
    exec gunicorn nav_info.asgi:application \
        -k uvicorn.workers.UvicornWorker \
        --access-logfile - \
        --name nav_info \
        --bind 0.0.0.0:8000 \
        --max-requests 200 \
        --workers=3
fi
fi
