@echo off
chcp 65001 >nul 2>&1
title QT MCP Client

echo ==========================================
echo QT MCP Client - Windows Launcher
echo ==========================================
echo.

:: Check Python availability
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found, please install Python 3.8+
    pause
    exit /b 1
)

:: Change to script directory
cd /d "%~dp0"

:: Check dependencies
echo Checking dependencies...
pip show python-dotenv >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

:: Start client
echo Starting MCP Client...
echo.
python start.py

echo.
echo Client exited, press any key to close...
pause >nul 