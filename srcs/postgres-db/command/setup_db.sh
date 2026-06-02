#!/bin/sh

export PGDATA=/var/lib/postgresql/data

if [ ! -d "$PGDATA/base" ]; then
    echo "Initializing database storage..."
    initdb
fi

echo "Starting PostgreSQL in the foreground..."
exec postgres -h "*"
