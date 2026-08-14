#!/bin/bash
echo "Preparing app ..."

# Create the virtual network
echo "Creating network 'mindflow-network'..."
docker network create mindflow-network || true

# Create the persistent named volume
echo "Creating persistent volume 'mindflow-db-data'..."
docker volume create mindflow-db-data || true

# Build custom web application image
echo "Building web service image 'mindflow-web'..."
docker build -t mindflow-web:latest .

echo "Preparation complete! Ready to start the application."