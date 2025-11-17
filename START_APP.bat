@echo off
echo ========================================
echo Real Estate Platform - Quick Start
echo RIVERHEDGE PARTNERS LIMITED
echo ========================================
echo.

echo Starting Backend Server...
start "Django Backend" cmd /k "cd /d "%~dp0" && venv\Scripts\activate && python manage.py runserver"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "React Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo Application is starting...
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/api/docs/
echo.
echo Press any key to open the application in your browser...
pause >nul

start http://localhost:5173

echo.
echo ========================================
echo Application is running!
echo.
echo To stop the servers, close the terminal windows.
echo ========================================

