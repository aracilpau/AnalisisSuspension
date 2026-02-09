# Guía de Instalación y Primeros Pasos

## Requisitos del Sistema

- Python 3.7 o superior
- pip (gestor de paquetes de Python)
- Sistema operativo: Windows, macOS o Linux

## Instalación

### 1. Instalar Python (si no lo tienes)

#### Windows:
1. Ve a [python.org/downloads](https://www.python.org/downloads/)
2. Descarga Python 3.10 o superior
3. **IMPORTANTE:** Durante la instalación, marca la casilla "Add Python to PATH"
4. Completa la instalación

#### Verificar instalación:
Abre PowerShell o CMD y ejecuta:

```powershell
python --version
```

o

```powershell
py --version
```

Deberías ver algo como `Python 3.x.x`.

### 2. Instalar Dependencias

#### Opción A: Script Automático (Windows - Recomendado)

Simplemente ejecuta el script de instalación:

```powershell
.\install.bat
```

o haz doble clic en el archivo `install.bat` desde el explorador de archivos.

#### Opción B: Manual

Abre PowerShell o CMD en el directorio del proyecto y ejecuta:

**En Windows:**
```powershell
python -m pip install -r requirements.txt
```

o si eso no funciona:
```powershell
py -m pip install -r requirements.txt
```

**En Linux/Mac:**
```bash
pip install -r requirements.txt
```

o

```bash
pip3 install -r requirements.txt
```

Esto instalará:
- NumPy (cálculos numéricos)
- Matplotlib (visualización)
- SciPy (resolución numérica)

### 3. Verificar Instalación

Ejecuta el script de prueba básico:

```bash
python test_basic.py
```

Si ves "✓ TODOS LOS TESTS PASARON EXITOSAMENTE", la instalación es correcta.

## Primer Uso

### Ejecutar el Programa

```bash
python main.py
```

### Flujo Básico

1. **Seleccionar Geometría:**
   - Opción 1-5: Usar una configuración predefinida (sportbike, enduro, etc.)
   - Opción 6: Introducir geometría personalizada

2. **Menú Principal:** El programa presenta 7 opciones:
   - **Opción 1:** Visualizar geometría en una posición específica
   - **Opción 2:** Analizar curva completa de leverage ratio
   - **Opción 3:** Ver animación del movimiento
   - **Opción 4:** Calcular LR en un punto específico
   - **Opción 5:** Exportar datos a CSV
   - **Opción 6:** Cambiar geometría
   - **Opción 7:** Ver resumen de configuración

## Ejemplo de Uso Rápido

### Análisis Básico de Sportbike

```bash
python main.py

# En el menú de configuración:
1  # Seleccionar sportbike

# En el menú principal:
2  # Analizar curva de leverage ratio
# Presiona Enter para usar valores por defecto (-50 a 50 mm)
# Se mostrará el análisis y gráficos
```

### Crear Geometría Personalizada

```bash
python main.py

# En el menú de configuración:
6  # Geometría personalizada

# Introduce valores (o Enter para usar defaults):
# - Longitud basculante: 620
# - Ángulo inicial: 13
# - Anclaje shock en basculante X: 210
# - Anclaje shock en basculante Y: 65
# - Anclaje shock en chasis X: 125
# - Anclaje shock en chasis Y: 245
# - Radio rueda: 310
```

## Interpretar Resultados

### Leverage Ratio (LR)

El leverage ratio indica cuánto se mueve la rueda por cada unidad de movimiento del amortiguador:

- **LR = 2.5:** La rueda se mueve 2.5 mm por cada 1 mm del shock
- **LR más alto:** Suspensión más "suave" (menos fuerza transmitida al shock)
- **LR más bajo:** Suspensión más "directa" (más fuerza al shock)

### Progresividad

El porcentaje de progresividad indica cómo cambia el LR durante la compresión:

- **Positivo (>5%):** Sistema PROGRESIVO
  - El LR aumenta en compresión
  - Más suave al inicio, más rígido al final
  - Mejor para absorber impactos grandes

- **Negativo (<-5%):** Sistema REGRESIVO
  - El LR disminuye en compresión
  - Más rígido al inicio, más suave al final
  - Poco común, puede causar problemas de control

- **Cerca de 0 (-5% a 5%):** Sistema LINEAL
  - LR constante
  - Comportamiento predecible
  - Más fácil de configurar

## Solución de Problemas

### Error: "Module not found"

Asegúrate de ejecutar el programa desde el directorio raíz del proyecto:

```bash
cd c:\Users\GorkaAracil\OneDrive\Documents\projects\motorstudent
python main.py
```

### Error: "numpy not found" u otra librería

Reinstala las dependencias:

```bash
pip install -r requirements.txt --force-reinstall
```

### Gráficos no se muestran

Si estás en un sistema sin interfaz gráfica (servidor), no podrás ver los gráficos directamente. Usa la opción 5 para exportar datos y analízalos en otro sistema.

### Valores de LR inusuales

Si obtienes leverage ratios muy altos (>10) o muy bajos (<0.5), verifica:
- Las coordenadas del anclaje del shock
- Que el ángulo del basculante sea razonable
- Que las unidades sean correctas (todo en milímetros)

## Exportar y Analizar Datos

### Exportar a CSV

```bash
# En el menú principal, opción 5
5
# Introduce nombre de archivo: mi_analisis
# Rango: -50 a 50 mm
# Número de puntos: 200
```

Esto genera `mi_analisis.csv` con columnas:
- Wheel_Travel_mm: Desplazamiento de rueda
- Shock_Travel_mm: Desplazamiento de shock
- Leverage_Ratio: Ratio instantáneo
- Shock_Velocity_Relative: Velocidad relativa (1/LR)

### Usar Datos en Excel/Hojas de Cálculo

1. Abre el archivo CSV en Excel/LibreOffice
2. Crea gráficos personalizados
3. Compara diferentes configuraciones
4. Calcula métricas adicionales

## Próximos Pasos

1. **Experimentar con Diferentes Configuraciones:**
   - Prueba todas las configuraciones predefinidas
   - Modifica parámetros y observa los cambios

2. **Optimizar tu Suspensión:**
   - Analiza la configuración actual de tu moto
   - Introduce los valores reales
   - Compara con configuraciones de referencia

3. **Documentar Resultados:**
   - Exporta datos de configuraciones prometedoras
   - Guarda gráficos (botón guardar en ventana matplotlib)
   - Compara antes/después de modificaciones

## Contacto y Soporte

Para preguntas o problemas, contacta al equipo MotorStudent.

## Notas Importantes

- Todas las medidas están en milímetros (mm)
- Los ángulos se introducen en grados, pero se convierten a radianes internamente
- El sistema de coordenadas tiene origen en el pivote del basculante
- Los valores por defecto están optimizados para motos de competición típicas
