#!/bin/bash

PORT=${PORT:-8898}

echo "Waiting for database..."
python -m ai_metaphors.server.db.init_db

echo "Starting server..."
cd /app
gunicorn --bind 0.0.0.0:${PORT} --workers 4 --timeout 3600 --worker-class uvicorn.workers.UvicornWorker ai_metaphors.server.main:app