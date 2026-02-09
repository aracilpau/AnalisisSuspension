@echo off
echo ======================================================================
echo   Analizador de Cinematica de Suspensiones - Equipo MotorStudent
echo ======================================================================
echo.

REM Intentar con 'python'
python --version >nul 2>&1
if %errorlevel% equ 0 (
    python main.py
    goto end
)

REM Intentar con 'py'
py --version >nul 2>&1
if %errorlevel% equ 0 (
    py main.py
    goto end
)

REM Si llegamos aqui, Python no esta instalado
echo [ERROR] Python no esta instalado en tu sistema
echo.
echo Por favor:
echo 1. Instala Python desde https://www.python.org/downloads/
echo 2. Ejecuta 'install.bat' para instalar dependencias
echo 3. Ejecuta este script de nuevo
echo.
pause
exit /b 1

:end
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul
