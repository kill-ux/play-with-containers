#!/bin/bash

set -euo pipefail

echo "=== Setting up Docker and Docker Compose ===";

# Import Docker’s Official GPG Key
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod +r /etc/apt/keyrings/docker.asc

# Add the Docker APT Repository
tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

# Install Docker Engine and Docker Compose
apt-get update
apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin make

# add user vagrant to docker group
usermod -aG docker vagrant

echo "=== Done setting up Docker and Docker Compose ===";