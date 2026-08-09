@echo off
REM Start backend (FastAPI) on 8001 and Nuxt dev on 3000 for Playwright E2E
cd /d D:\dev\ChenXuBlog\backend
start "chenxu-backend" .venv\Scripts\uvicorn.exe backend:app --host 127.0.0.1 --port 8001
cd /d D:\dev\ChenXuBlog\frontend
start "chenxu-nuxt" cmd /c npx nuxt dev --host 127.0.0.1 --port 3000
echo Both servers starting. Backend:8001 Nuxt:3000
