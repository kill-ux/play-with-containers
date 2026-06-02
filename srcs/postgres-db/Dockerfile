FROM alpine:latest

RUN apk update && apk add --no-cache postgresql


COPY command/setup_db.sh /tmp/setup_db.sh

RUN chmod +x /tmp/setup_db.sh && \
    chown postgres:postgres /tmp/setup_db.sh && \
    mkdir -p /run/postgresql && \
    chown -R postgres:postgres /run/postgresql

USER postgres

ENTRYPOINT [ "/tmp/setup_db.sh" ]
