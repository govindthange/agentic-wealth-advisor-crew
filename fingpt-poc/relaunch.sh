#!/bin/bash
# Rebuilds and restarts all docker-compose services
set -e
docker compose down --remove-orphans
echo "Relaunching Docker Compose stack..."
docker compose up -d --build --force-recreate
echo "Done!"
