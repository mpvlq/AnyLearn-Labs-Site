@echo off
echo ========================================
echo AnyLearn Labs - Quick Setup Script
echo ========================================
echo.

echo [1/6] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

echo [2/6] Activating virtual environment...
call venv\Scripts\activate
echo.

echo [3/6] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo [4/6] Creating environment file...
if not exist .env (
    copy .env.example .env
    echo .env file created! Please edit it with your settings.
) else (
    echo .env file already exists, skipping...
)
echo.

echo [5/6] Running database migrations...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)
echo Migrations completed successfully!
echo.

echo [6/6] Creating superuser...
echo.
echo Please create an admin account:
python manage.py createsuperuser
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the server, run:
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Then visit:
echo   - Main site: http://127.0.0.1:8000/
echo   - Admin: http://127.0.0.1:8000/admin/
echo.
pause
