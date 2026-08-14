#!/bin/bash
echo "Running app ..."

# Remove existing containers if they exist to allow clean restarts
docker rm -f mindflow-db mindflow-web >/dev/null 2>&1 || true

# Start PostgreSQL Database container
echo "Starting Database Service (PostgreSQL)..."
docker run -d \
  --name mindflow-db \
  --network mindflow-network \
  -p 5432:5432 \
  -v mindflow-db-data:/var/lib/postgresql/data \
  -e POSTGRES_DB=mindflow \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secretpassword \
  --restart on-failure \
  postgres:15-alpine

# Start Flask Web App container
echo "Starting Web Service (Flask)..."
docker run -d \
  --name mindflow-web \
  --network mindflow-network \
  -p 5000:5000 \
  -e DB_HOST=mindflow-db \
  -e DB_USER=admin \
  -e DB_PASSWORD=secretpassword \
  -e DB_NAME=mindflow \
  --restart on-failure \
  mindflow-web:latest

echo ""
echo "=========================================================="
echo " The app is available at http://localhost:5000"
echo "=========================================================="