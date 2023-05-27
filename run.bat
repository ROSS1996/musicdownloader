@echo off

rem Check if python3 command exists
where python3 >nul 2>nul
if %errorlevel% equ 0 (
    python3 music.py
    echo Press any key to exit...
    pause >nul
    exit /b
)

rem Check if python command exists
where python >nul 2>nul
if %errorlevel% equ 0 (
    python --version 2>&1 | findstr /C:"Python 3." >nul
    if %errorlevel% equ 0 (
        python music.py
        echo Press any key to exit...
        pause >nul
        exit /b
    )
)

echo Python 3 is not installed. Try installing it using pythonpip.bat and try again
pause >nul
exit /b 1
