#!/bin/bash
# Start the backend and frontend services in the background
docker-compose up -d backend frontend

# Wait for the services to start
sleep 10

# Build and run the backend-tests service
docker-compose up --build backend-tests

# Stop the backend and frontend services after running the tests
docker-compose down
