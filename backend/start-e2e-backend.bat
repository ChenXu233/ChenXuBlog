@echo off
REM Start backend with isolated E2E test database on port 8001
REM Usage: start-e2e-backend.bat [fresh]
setlocal
cd /d %~dp0

if "%1"=="fresh" (
  del /q data\e2e_blog.db 2>nul
  echo Fresh E2E database created
)

set DATABASE_URI=sqlite+aiosqlite:///./data/e2e_blog.db
set MINIO_ENABLED=false
set MAIL_ENABLED=false

.venv\Scripts\uvicorn.exe backend:app --host 127.0.0.1 --port 8001
