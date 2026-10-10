@echo off
title CLYMEX AI - Predict Risk. Protect Tomorrow.
echo ====================================================================
echo  CLYMEX AI - Climate Intelligence Platform (Mozambique Demonstrator)
echo  "Predict Risk. Protect Tomorrow."
echo ====================================================================
echo.

echo [1/2] Iniciando Backend FastAPI na porta 8000...
start "CLYMEX AI Backend" cmd /k "set PYTHONPATH=backend && .\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo [2/2] Iniciando Frontend Next.js na porta 3000...
start "CLYMEX AI Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ====================================================================
echo  CLYMEX AI esta em execucao!
echo  Frontend WebGIS:   http://localhost:3000
echo  API Docs (Swagger): http://localhost:8000/docs
echo ====================================================================
pause
