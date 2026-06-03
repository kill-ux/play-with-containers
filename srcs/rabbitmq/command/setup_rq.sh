#!/bin/sh
set -euo pipefail

rabbitmqctl add_user $RABBITMQ_USER $RABBITMQ_PASS || true
rabbitmqctl set_permissions -p / $RABBITMQ_USER ".*" ".*" ".*" || true