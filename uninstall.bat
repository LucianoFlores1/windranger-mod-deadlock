@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo =======================================================
echo   Desinstalador de Mod: Windranger sobre Grey Talon
echo =======================================================
echo.

set "CITADEL_DIR="

if exist "E:\SteamLibrary\steamapps\common\Deadlock\game\citadel" (
    set "CITADEL_DIR=E:\SteamLibrary\steamapps\common\Deadlock\game\citadel"
)
if not defined CITADEL_DIR if exist "C:\Program Files (x86)\Steam\steamapps\common\Deadlock\game\citadel" (
    set "CITADEL_DIR=C:\Program Files (x86)\Steam\steamapps\common\Deadlock\game\citadel"
)
if not defined CITADEL_DIR if exist "D:\SteamLibrary\steamapps\common\Deadlock\game\citadel" (
    set "CITADEL_DIR=D:\SteamLibrary\steamapps\common\Deadlock\game\citadel"
)
if not defined CITADEL_DIR if exist "F:\SteamLibrary\steamapps\common\Deadlock\game\citadel" (
    set "CITADEL_DIR=F:\SteamLibrary\steamapps\common\Deadlock\game\citadel"
)

if not defined CITADEL_DIR (
    set /p "CITADEL_DIR=Ingresa la ruta de la carpeta 'citadel': "
)

set "TARGET_VPK=%CITADEL_DIR%\addons\pak02_dir.vpk"

if exist "%TARGET_VPK%" (
    del /F /Q "%TARGET_VPK%"
    echo [EXITO] Se ha eliminado pak02_dir.vpk de %CITADEL_DIR%\addons.
    echo Grey Talon volvera a su modelo original por defecto.
) else (
    echo [INFO] El archivo pak02_dir.vpk no estaba instalado en "%TARGET_VPK%".
)

echo.
pause
