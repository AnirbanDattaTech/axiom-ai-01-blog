@echo off
title Axiom LDE Generator
echo [1/3] Waking up the LDE Generator...

:: This ensures the script runs exactly in the folder where the .bat file lives
cd /d "%~dp0"

ECHO [2/3] Activating Conda Environment 'aaicore'...
CALL "C:\Users\Admin\miniconda3\Scripts\activate.bat"
CALL conda activate aaicore

IF ERRORLEVEL 1 (
    ECHO.
    ECHO ERROR: Could not activate 'aai'.
    PAUSE
    GOTO :EOF
)
ECHO      ...Environment Active.
ECHO.
ECHO [3/3] Creating LDE map...

:: Run the script with default settings (All subfolders, Depth 4, AI Mode)
python project_structure_master.py --mode crystal --depth 5

:: If you prefer AI mode as your 1-click default, use this line instead:
:: python project_structure_master.py

echo.
pause