#!/bin/sh
set -euo pipefail

rabbitmqctl add_user rabbit_user password || true
rabbitmqctl set_permissions -p / rabbit_user ".*" ".*" ".*" || true