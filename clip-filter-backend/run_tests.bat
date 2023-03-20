@echo off
docker-compose up -d backend frontend
timeout /t 10 /nobreak
docker-compose up --build backend-tests
docker-compose down
pause