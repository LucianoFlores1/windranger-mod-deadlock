@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo =======================================================
echo   Instalador de Mod: Windranger sobre Grey Talon
echo =======================================================
echo.

set "MOD_VPK=%~dp0build\pak02_dir.vpk"

if not exist "%MOD_VPK%" (
    echo [ERROR] No se encontro "%MOD_VPK%".
    echo Por favor asegurate de no mover este instalador de la carpeta del proyecto.
    pause
    exit /b 1
)

set "CITADEL_DIR="

:: 1. Verificar ruta de este equipo
if exist "E:\SteamLibrary\steamapps\common\Deadlock\game\citadel" (
    set "CITADEL_DIR=E:\SteamLibrary\steamapps\common\Deadlock\game\citadel"
)

:: 2. Verificar rutas estandar de Steam
if not defined CITADEL_DIR if exist "C:\Program Files (x86)\Steam\steamapps\common\Deadlock\game\citadel" (
    set "CITADEL_DIR=C:\Program Files (x86)\Steam\steamapps\common\Deadlock\game\citadel"
)

if not defined CITADEL_DIR if exist "D:\SteamLibrary\steamapps\common\Deadlock\game\citadel" (
    set "CITADEL_DIR=D:\SteamLibrary\steamapps\common\Deadlock\game\citadel"
)

if not defined CITADEL_DIR if exist "F:\SteamLibrary\steamapps\common\Deadlock\game\citadel" (
    set "CITADEL_DIR=F:\SteamLibrary\steamapps\common\Deadlock\game\citadel"
)

:: 3. Si no se detecta automaticamente, solicitar ruta al usuario
if not defined CITADEL_DIR (
    echo No se detecto Deadlock en las rutas por defecto.
    set /p "CITADEL_DIR=Ingresa la ruta completa de la carpeta 'citadel' (ej: C:\Steam\steamapps\common\Deadlock\game\citadel): "
)

if not exist "%CITADEL_DIR%" (
    echo [ERROR] La carpeta ingresada no existe: "%CITADEL_DIR%"
    pause
    exit /b 1
)

set "ADDONS_DIR=%CITADEL_DIR%\addons"
if not exist "%ADDONS_DIR%" (
    echo Creando carpeta de addons en: %ADDONS_DIR% ...
    mkdir "%ADDONS_DIR%"
)

echo Copiando mod a: %ADDONS_DIR%\pak02_dir.vpk ...
copy /Y "%MOD_VPK%" "%ADDONS_DIR%\pak02_dir.vpk" > nul

if %ERRORLEVEL% equ 0 (
    echo.
    echo =======================================================
    echo  [EXITO] Mod instalado correctamente como pak02_dir.vpk
    echo =======================================================
    echo.
    echo RECORDATORIO:
    echo Asegurate de que en "%CITADEL_DIR%\gameinfo.gi"
    echo este agregada la linea 'Game    citadel/addons' en SearchPaths.
    echo Revisa el archivo README.md para ver el tutorial de 1 minuto.
) else (
    echo [ERROR] Hubo un problema al copiar el archivo.
)

echo.
pause
