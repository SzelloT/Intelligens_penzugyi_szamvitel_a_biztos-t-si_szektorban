@echo off
cd /d "%~dp0"
title Sony A7 IV Chatbot Indito

:: 1. Keresés a PyCharm virtuális környezetében
if exist ".venv\Scripts\python.exe" (
    set "PY_CMD=.venv\Scripts\python.exe"
    goto RUN
)
if exist "venv\Scripts\python.exe" (
    set "PY_CMD=venv\Scripts\python.exe"
    goto RUN
)

:: 2. Keresés a Windows beépített 'py' indítójával
py --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py"
    goto RUN
)

:: 3. Keresés a standard 'python' paranccsal
python --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=python"
    goto RUN
)

echo HIBA: Nem talalhato Python sem a mappaban, sem a rendszerben!
echo Futtassa a kodot inkabb kozvetlenul a PyCharm-bol (Jobb klikk -> Run).
pause
exit /b

:RUN
echo Python megtalalva: %PY_CMD%
echo [1/2] Fuggosegek ellenorzese...
%PY_CMD% -m pip install requests >nul 2>&1

echo [2/2] SZT_SonyA7IV_Chatbot_Html.py inditasa...
%PY_CMD% SZT_SonyA7IV_Chatbot_Html.py
pause