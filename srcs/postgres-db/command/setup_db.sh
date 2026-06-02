#!/bin/sh
export PGDATA=/var/lib/postgresql/data

if [ ! -d "$PGDATA/base" ]; then
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
