@echo off
echo ========================================
echo    Local AI Writer Setup Script
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

:: Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo ✅ Python and Node.js are installed
echo.

:: Setup backend
echo 🔧 Setting up backend...
cd backend

:: Create virtual environment
echo Creating Python virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✅ Backend setup complete
echo.

:: Setup frontend
echo 🔧 Setting up frontend...
cd ..\frontend

:: Install Node.js dependencies
echo Installing Node.js dependencies...
npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo ✅ Frontend setup complete
echo.

:: Go back to root directory
cd ..

echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Download the model: cd backend ^&^& python download_model.py
echo 2. Start backend: cd backend ^&^& venv\Scripts\activate ^&^& uvicorn app:app --reload
echo 3. Start frontend: cd frontend ^&^& npm start
echo.
echo The application will be available at http://localhost:3000
echo.
pause
