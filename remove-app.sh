#!/bin/bash
echo "Removing app resources ..."

# Stop and remove containers
echo "Removing containers..."
docker rm -f mindflow-web mindflow-db || true

# Remove network
echo "Removing network..."
docker network rm mindflow-network || true

# Remove volume
echo "Removing volume..."
docker volume rm mindflow-db-data || true

# Remove image
echo "Removing custom image..."
docker rmi mindflow-web:latest || true

echo "Removed app."