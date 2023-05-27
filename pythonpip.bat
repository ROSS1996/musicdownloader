@echo off

rem Check if Python 3 is installed
where python3 > nul 2>&1 || where python > nul 2>&1 && (
    python --version 2>&1 | findstr /C:"Python 3." > nul && (
        echo Python 3 is already installed.
    ) || (
        rem Download and install Python 3 using PowerShell
        echo Python is not installed. Installing Python 3...
        powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe' -OutFile 'python_installer.exe'; Start-Process -Wait -FilePath 'python_installer.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1'; Remove-Item -Path 'python_installer.exe'"
        rem Check if Python installation was successful
        where python > nul 2>&1
        if %errorlevel% neq 0 (
            echo Failed to install Python. Please install Python manually.
            echo Press any key to exit...
            pause >nul
            exit /b 1
        )
        echo Python 3 has been installed successfully.
    )
)

rem Check if PIP is installed
where pip3 > nul 2>&1
if %errorlevel% equ 0 (
    echo Pip is already installed.
    echo Press any key to exit...
    pause >nul
    exit /b
) else (
    rem Check if PIP is installed
    where pip > nul 2>&1
    if %errorlevel% equ 0 (
        echo Pip is already installed.
        echo Press any key to exit...
        pause >nul
        exit /b
    ) else (
        echo Pip is not installed. Installing pip using 'python -m ensurepip --upgrade'...
        python -m ensurepip --upgrade
        if %errorlevel% neq 0 (
            echo Failed to install pip using 'python -m ensurepip --upgrade'. Trying 'python3 -m ensurepip --upgrade'...
            python3 -m ensurepip --upgrade
            if %errorlevel% neq 0 (
                echo Failed to install pip using 'python3 -m ensurepip --upgrade'. Please install pip manually.
                echo Opening the installation guide in your default browser...
                start "" "https://pip.pypa.io/en/stable/installation/"
                echo Press any key to exit...
                pause >nul
                exit /b 1
            )
        )
    )
)



