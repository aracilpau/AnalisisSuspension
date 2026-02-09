# Guía Rápida para Windows

## Instalación en 3 Pasos

### Paso 1: Instalar Python

Si no tienes Python instalado:

1. Ve a [python.org/downloads](https://www.python.org/downloads/)
2. Descarga la última versión (Python 3.10 o superior)
3. **MUY IMPORTANTE:** Durante la instalación, marca la casilla **"Add Python to PATH"**
4. Completa la instalación

### Paso 2: Instalar Dependencias

Haz doble clic en el archivo:
```
install.bat
```

O desde PowerShell/CMD:
```powershell
.\install.bat
```

Esto instalará automáticamente NumPy, Matplotlib y SciPy.

### Paso 3: Ejecutar el Programa

Haz doble clic en el archivo:
```
run.bat
```

O desde PowerShell/CMD:
```powershell
.\run.bat
```

## Verificar Instalación

Para asegurarte de que todo está correcto, ejecuta:
```
test.bat
```

Deberías ver: "✓ TODOS LOS TESTS PASARON EXITOSAMENTE"

## Solución de Problemas en Windows

### Error: "Python no está instalado"

**Solución:**
1. Instala Python desde [python.org](https://www.python.org/downloads/)
2. **IMPORTANTE:** Marca "Add Python to PATH" durante la instalación
3. Reinicia la terminal o PowerShell
4. Ejecuta `install.bat` de nuevo

### Error: "pip no se reconoce"

**Solución:**

Abre PowerShell y ejecuta:
```powershell
python -m pip install -r requirements.txt
```

Si eso no funciona:
```powershell
py -m pip install -r requirements.txt
```

### Error: "module not found" al ejecutar

**Solución:**

Asegúrate de estar en el directorio correcto:
```powershell
cd c:\Users\GorkaAracil\OneDrive\Documents\projects\motorstudent
python main.py
```

### Python instalado pero no en PATH

**Solución:**

Si instalaste Python pero olvidaste marcar "Add to PATH":

1. Busca "Environment Variables" en el menú de Windows
2. Edita las variables de entorno del sistema
3. En "Path", añade las rutas de Python (ejemplo):
   - `C:\Users\TuUsuario\AppData\Local\Programs\Python\Python310\`
   - `C:\Users\TuUsuario\AppData\Local\Programs\Python\Python310\Scripts\`
4. Reinicia PowerShell

O reinstala Python marcando "Add to PATH"

## Uso Rápido

### Análisis de Sportbike

1. Ejecuta `run.bat`
2. Presiona `1` (seleccionar sportbike)
3. Presiona `2` (analizar curva leverage ratio)
4. Presiona Enter para valores por defecto
5. Se mostrarán gráficos y resultados

### Introducir tu Propia Geometría

1. Ejecuta `run.bat`
2. Presiona `6` (geometría personalizada)
3. Introduce los valores de tu moto (en milímetros):
   - Longitud del basculante
   - Ángulo inicial
   - Posiciones de anclajes del amortiguador
   - Radio de rueda
4. Analiza con las opciones del menú

### Exportar Datos

1. En el menú principal, presiona `5`
2. Introduce nombre del archivo (sin extensión)
3. Define rango de análisis
4. Se creará un archivo CSV con todos los datos

## Comandos Útiles

### Ejecutar programa directamente:
```powershell
python main.py
```
o
```powershell
py main.py
```

### Ejecutar tests:
```powershell
python test_basic.py
```

### Instalar/actualizar dependencias:
```powershell
python -m pip install -r requirements.txt --upgrade
```

## Archivos Importantes

- **install.bat** - Instala dependencias automáticamente
- **run.bat** - Ejecuta el programa principal
- **test.bat** - Ejecuta pruebas de validación
- **main.py** - Programa principal (también se puede ejecutar directamente)
- **requirements.txt** - Lista de dependencias de Python

## ¿Qué hace cada opción del menú?

1. **Visualizar geometría** - Muestra un diagrama de la suspensión en una posición específica
2. **Analizar curva de leverage ratio** - Calcula y grafica el comportamiento a lo largo del recorrido
3. **Animar movimiento** - Muestra una animación del movimiento de la suspensión
4. **Calcular LR en posición específica** - Obtiene el leverage ratio en un punto concreto
5. **Exportar datos a CSV** - Guarda todos los datos de análisis en formato CSV
6. **Modificar geometría** - Cambia la configuración de la suspensión
7. **Mostrar resumen** - Muestra información de la configuración actual

## Ejemplo Completo de Uso

```
1. Doble clic en run.bat
2. Seleccionar opción 1 (sportbike)
3. En menú principal, opción 7 (ver resumen)
4. Opción 2 (analizar curva)
5. Presionar Enter (usar defaults -50 a 50 mm)
6. Ver gráficos
7. Cerrar gráfico
8. Opción 5 (exportar)
9. Nombre: "sportbike_analisis"
10. Ver archivo sportbike_analisis.csv creado
```

## Próximos Pasos

Una vez instalado y funcionando:

1. **Familiarízate** probando todas las configuraciones predefinidas
2. **Introduce** los valores reales de tu moto de competición
3. **Experimenta** modificando parámetros y observando los cambios
4. **Optimiza** buscando el leverage ratio y progresividad ideales
5. **Documenta** exportando datos de tus mejores configuraciones

## Contacto

Para dudas o problemas, contacta al equipo MotorStudent.

---

**¡Listo para empezar! Ejecuta `install.bat` y luego `run.bat`**
