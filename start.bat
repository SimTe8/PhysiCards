@echo off
title PhysiCards - Physik Karteikarten Software
echo ============================================================
echo   PhysiCards - Physik Karteikarten ^& Formeltrainer
echo ============================================================
echo Starte Anwendung...
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ein Fehler ist aufgetreten. Versuche Browser-Modus...
    python main.py --browser
)
pause

