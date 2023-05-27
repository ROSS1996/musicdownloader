@echo off

rem Check if 'pip' command exists
where pip > nul 2>&1
if %errorlevel% equ 0 (
    pip install --upgrade -r requirements.txt
    exit /b
) else (
    rem Check if 'pip3' command exists
    where pip3 > nul 2>&1
    if %errorlevel% equ 0 (
        pip3 install --upgrade -r requirements.txt
        exit /b
    ) else (
        echo Pip is not installed. Try installing it using the pythonpip.sh installer and try again.
        pause >nul
        exit /b 1
    )
)
