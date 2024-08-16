#!/bin/bash

set -e
chmod +x entrypoint.sh

echo "Creating Database"
# Run the table creation script
python3 create_tables.py

echo "Running FastAPI"
# Start the Uvicorn server
uvicorn api:app --host 0.0.0.0 --port 8080