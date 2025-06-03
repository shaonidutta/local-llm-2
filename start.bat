@echo off
echo ========================================
echo    Starting Local AI Writer
echo ========================================
echo.

:: Check if setup has been run
if not exist "backend\venv" (
    echo ❌ Backend not set up. Please run setup.bat first.
    pause
    exit /b 1
)

if not exist "frontend\node_modules" (
    echo ❌ Frontend not set up. Please run setup.bat first.
    pause
    exit /b 1
)

echo 🚀 Starting Local AI Writer...
echo.

:: Start backend in a new window
echo Starting backend server...
start "AI Writer Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn app:app --reload --host 0.0.0.0 --port 8000"

:: Wait a moment for backend to start
timeout /t 3 /nobreak >nul

:: Start frontend in a new window
echo Starting frontend server...
start "AI Writer Frontend" cmd /k "cd frontend && npm start"

echo.
echo ✅ Both servers are starting...
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit this window...
pause >nul
