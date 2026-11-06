@echo off
chcp 65001 > nul
echo =======================================================
echo   Compilador de Mod: Windranger sobre Grey Talon
echo =======================================================
echo.

python "%~dp0tools\build_mod.py"

echo.
pause
