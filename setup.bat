@echo off
echo ========================================
echo Smart Document Manager - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo.
echo Installing dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
echo [OK] Dependencies installed

REM Check if .env exists
if not exist ".env" (
    echo.
    echo Creating .env file from template...
    copy .env.example .env
    echo [WARNING] Please edit .env and add your:
    echo    - DATABASE_URL (PostgreSQL connection string)
    echo    - OPENAI_API_KEY (from https://platform.openai.com/api-keys)
    echo.
    pause
)

REM Create necessary directories
echo.
echo Creating directories...
if not exist "uploads" mkdir uploads
if not exist "chroma_db" mkdir chroma_db
echo [OK] Directories created

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To start the application:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run the app: python app.py
echo   3. Open browser: http://localhost:5000
echo.
echo Make sure PostgreSQL is installed and running!
echo.
pause
