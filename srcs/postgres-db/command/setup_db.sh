#!/bin/sh
set -euo pipefail

export PGDATA=/var/lib/postgresql/main

# if [ -z ${DB_USER:-} ] || [ -z ${DB_PASS:-} ] || [ -z ${DB_NAME:-} ]; then
#     echo "ERROR: DB_USER, DB_PASS, and DB_NAME environment variables must be set!"
#     exit 1
# fi

echo "#######################################"
ls /var/lib/postgresql/17

PG_VERSION=$(ls /usr/lib/postgresql | grep -E '^[0-9]+$')
export PATH="/usr/lib/postgresql/$PG_VERSION/bin:$PATH"

if [ ! -d "$PGDATA/base" ]; then
    mkdir -p "$PGDATA"

    echo "Initializing database storage..."
    initdb

    echo "local all all trust" > "$PGDATA/pg_hba.conf"
    echo "host all all 0.0.0.0/0 scram-sha-256" >> "$PGDATA/pg_hba.conf"

    echo "Starting temporary cluster for setup..."
    postgres -k /run/postgresql &
    TEMP_PID=$!

    until pg_isready ; do
        echo "Waiting for database to start..."
        sleep 0.25
    done

    echo "Configuring roles and databases..."
    psql -c "ALTER USER postgres WITH PASSWORD '$DB_PASS';"
    psql -c "CREATE USER $DB_USER WITH SUPERUSER PASSWORD '$DB_PASS';"
    createdb -O $DB_USER $DB_NAME

    echo "Shutting down temporary setup cluster..."
    kill $TEMP_PID
    wait $TEMP_PID
fi

echo "Starting PostgreSQL in the foreground..."
exec postgres -h "*"
