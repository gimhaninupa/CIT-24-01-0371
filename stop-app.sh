#!/bin/bash
echo "Stopping app ..."

# Stop running containers
docker stop mindflow-web mindflow-db || true

echo "App paused. Containers stopped. Persistent data is preserved."