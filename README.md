

<div align="center">

# play-with-containers
<img src="res/17922_micros.png" width="50%" >

------

>  `play-with-containers` is a Docker Compose-based implementation of a microservices movie platform. It uses containerized Python services, two PostgreSQL databases, a RabbitMQ queue, and an API gateway to deliver a production-like multi-container architecture.
------

</div>



## Overview

This repository replaces the original Vagrant-based `crud-master` setup with Docker and Docker Compose, making deployment faster, reproducible, and easier to manage on Linux.

## Architecture

The application is built with the following services:

- `api-gateway`: forwards HTTP requests to inventory and billing services, and publishes billing orders to RabbitMQ.
- `inventory-app`: manages a movie inventory stored in a PostgreSQL database.
- `billing-app`: consumes billing order messages from RabbitMQ and stores order history in a separate PostgreSQL database.
- `inventory-db`: PostgreSQL database for inventory data.
- `billing-db`: PostgreSQL database for billing data.
- `billing-queue`: RabbitMQ server for asynchronous order processing.

All containers are connected through a single Docker bridge network and managed by `docker compose`.

## Key Features

- Multi-service Docker Compose deployment
- Separate PostgreSQL databases with persistent volumes
- RabbitMQ queue for asynchronous billing processing
- API gateway routing and message dispatching
- Automatic container restart on failure
- Environment-driven configuration via `.env`

## Prerequisites

- Docker Engine installed
- Docker Compose available (`docker compose`)
- Linux host (Ubuntu tested)

> [!IMPORTANT]
> we provide a vagrant file so you jaut need to install vagrnat binary and run `vagrnat up` with your best hypervisor like VirtualBox

## Setup

1. Copy environment variables:

```bash
cp .env.example .env
```

2. Review `.env` and update credentials if needed. Do not commit `.env`.

3. Build and start all containers:

```bash
docker compose up --build -d
```

4. Confirm services are running:

```bash
docker compose ps
```

5. Stop containers when finished:

```bash
docker compose stop
```

6. Remove containers and network while keeping volumes:

```bash
docker compose down
```

7. Remove containers, network, and volumes:

```bash
docker compose down -v
```

## Makefile Convenience Commands

Use the `Makefile` to simplify workflow:

- `make up` — build and start services
- `make stop` — stop services
- `make down` — stop and remove containers/networks
- `make clean` — remove containers, networks, and volumes
- `make prune` — remove unused Docker images

## Service Ports

Only the API gateway is exposed to the host.

- `api-gateway`: `3000`

Internal service ports:

- `inventory-app`: `8080`
- `billing-app`: `8080`
- `inventory-db`: `5432`
- `billing-db`: `5432`
- `billing-queue`: `5672`

The gateway is the only external entry point for requests.

## Persistent Volumes

Docker Compose defines persistent volumes for:

- `inventory_database` — inventory PostgreSQL data
- `billing_database` — billing PostgreSQL data
- `billing-queue-data` — RabbitMQ data
- `api-gateway-logs` — gateway access logs

## Environment Variables

The `.env.example` file contains the required configuration:

- `INVENTORY_DB_USER`
- `INVENTORY_DB_PASS`
- `INVENTORY_DB_NAME`
- `BILLING_DB_USER`
- `BILLING_DB_PASS`
- `BILLING_DB_NAME`
- `RABBITMQ_USER`
- `RABBITMQ_PASS`
- `RABBITMQ_QUEUE`
- `RABBITMQ_PORT`
- `INVENTORY_APP_PORT`
- `BILLING_APP_PORT`
- `APIGATEWAY_PORT`


## API Usage

All client requests should be sent through the API gateway at `http://localhost:3000`.

### Inventory endpoints

- List movies:

```bash
curl http://localhost:3000/api/movies/
```

- Add a movie:

```bash
curl -X POST http://localhost:3000/api/movies/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Interstellar", "description": "Space exploration"}'
```

- Get a movie by ID:

```bash
curl http://localhost:3000/api/movies/1
```

- Update a movie:

```bash
curl -X PUT http://localhost:3000/api/movies/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "New Title", "description": "Updated description"}'
```

- Delete a movie:

```bash
curl -X DELETE http://localhost:3000/api/movies/1
```

- Delete all movies:

```bash
curl -X DELETE http://localhost:3000/api/movies/
```

### Billing endpoints

- Submit a billing order:

```bash
curl -X POST http://localhost:3000/api/billing/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "123", "number_of_items": "2", "total_amount": "50.00"}'
```

- Retrieve processed orders:

```bash
curl http://localhost:3000/api/billing/
```

> The gateway forwards billing POST requests to RabbitMQ and returns `202 Accepted` once the order is queued.

## How It Works

- `api-gateway` proxies inventory CRUD requests to `inventory-app`.
- Billing POST requests are published to RabbitMQ by the gateway.
- `billing-app` consumes the queue and stores orders in `billing-db`.
- Both databases are isolated in separate PostgreSQL containers.
- Containers are restarted automatically with `restart: on-failure`.

## Notes

- The project is intentionally Docker-native; there is no Vagrant deployment required in this setup.
- All service images are built locally from the `srcs/*/Dockerfile` definitions.
- The API gateway is the only service exposed to the outside world.

## Troubleshooting

- If a service fails to start, inspect logs:

```bash
docker compose logs <service-name>
```

- To force rebuild after source changes:

```bash
docker compose build --no-cache
```

- If RabbitMQ is unavailable, ensure the `billing-queue` container is healthy and the `.env` variables are correct.

## Project Status

This repository now implements a clean Docker Compose microservices architecture for inventory management and asynchronous billing, replacing the previous Vagrant-based `crud-master` environment.
