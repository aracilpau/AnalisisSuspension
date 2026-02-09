@echo off
echo ======================================================================
echo   INSTALACION DE DEPENDENCIAS - Analizador de Cinematica de Suspensiones
echo ======================================================================
echo.

REM Intentar con 'python'
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python encontrado
    echo.
    echo Instalando dependencias...
    echo.
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo.
        echo ======================================================================
        echo   INSTALACION COMPLETADA EXITOSAMENTE
        echo ======================================================================
        echo.
        echo Ejecuta 'run.bat' o 'python main.py' para iniciar el programa.
        echo.
        goto end
    ) else (
        echo.
        echo [ERROR] Fallo en la instalacion de dependencias
        goto error
    )
)

REM Intentar con 'py'
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python encontrado (usando 'py')
    echo.
    echo Instalando dependencias...
    echo.
    py -m pip install --upgrade pip
    py -m pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo.
        echo ======================================================================
        echo   INSTALACION COMPLETADA EXITOSAMENTE
        echo ======================================================================
        echo.
        echo Ejecuta 'run.bat' o 'py main.py' para iniciar el programa.
        echo.
        goto end
    ) else (
        echo.
        echo [ERROR] Fallo en la instalacion de dependencias
        goto error
    )
)

REM Si llegamos aqui, Python no esta instalado
:nopython
echo.
echo [ERROR] Python no esta instalado en tu sistema
echo.
echo Por favor, instala Python 3.7 o superior desde:
echo https://www.python.org/downloads/
echo.
echo IMPORTANTE: Durante la instalacion, marca la casilla 'Add Python to PATH'
echo.
goto error

:error
echo.
echo ======================================================================
echo Presiona cualquier tecla para cerrar...
pause >nul
exit /b 1

:end
echo Presiona cualquier tecla para cerrar...
pause >nul
