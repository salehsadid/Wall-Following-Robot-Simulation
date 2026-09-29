@echo off
title WFR Simulator - Wall Following Robot
echo ========================================================
echo         Starting WFR Simulator (Emerald Theme)
echo ========================================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to PATH!
    echo Please install Python from https://www.python.org/
    echo and make sure to check "Add python.exe to PATH".
    echo.
    pause
    exit /b 1
)

:: Check if Pygame is installed, auto-install if missing
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Pygame not detected. Installing pygame automatically...
    pip install pygame
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install pygame. Please run 'pip install pygame' manually.
        pause
        exit /b 1
    )
    echo [INFO] Pygame installed successfully!
    echo.
)

:: Launch the simulator
echo Launching wfr_simulator.py...
python 2207024.py

if %errorlevel% neq 0 (
    echo.
    echo [INFO] Simulator closed with code %errorlevel%.
    pause
)
