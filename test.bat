@echo off
echo ======================================================================
echo   Prueba Basica del Sistema
echo ======================================================================
echo.

REM Intentar con 'python'
python --version >nul 2>&1
if %errorlevel% equ 0 (
    python test_basic.py
    goto end
)

REM Intentar con 'py'
py --version >nul 2>&1
if %errorlevel% equ 0 (
    py test_basic.py
    goto end
)

REM Si llegamos aqui, Python no esta instalado
echo [ERROR] Python no esta instalado en tu sistema
echo.
echo Por favor ejecuta 'install.bat' primero
echo.
pause
exit /b 1

:end
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul
