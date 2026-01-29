@echo off
echo 🚀 Jarvis AI Launcher - Python 3.10
echo ========================================

REM Set Python 3.10 path
set PYTHON310=C:\Users\omdar\AppData\Local\Programs\Python\Python310\python.exe

REM Check if Python 3.10 exists
if not exist "%PYTHON310%" (
    echo ❌ Python 3.10 not found at: %PYTHON310%
    echo Please install Python 3.10 or check the path
    pause
    exit /b 1
)

echo ✅ Found Python 3.10
echo 🔄 Starting Jarvis AI with Python 3.10...
echo.

REM Run Jarvis AI with Python 3.10
"%PYTHON310%" main.py

REM Keep window open if there was an error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Jarvis AI exited with error code: %ERRORLEVEL%
    pause
)
