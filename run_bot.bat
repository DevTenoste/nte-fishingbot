@echo off
title NTE Fishing Bot Launcher
:menu
cls
echo ===========================================
echo         NTE FISHING BOT LAUNCHER
echo ===========================================
echo.
echo 1. Calibrate (Set screen coordinates)
echo 2. Start Bot (Run AFK Fishing)
echo 3. Exit
echo.
set /p choice="Choose an option (1-3): "

if "%choice%"=="1" (
    echo Launching Calibration...
    python calibrate.py
    pause
    goto menu
)

if "%choice%"=="2" (
    echo Launching Fishing Bot...
    python fishing_bot.py
    pause
    goto menu
)

if "%choice%"=="3" (
    exit
)

echo Invalid choice, try again.
pause
goto menu
