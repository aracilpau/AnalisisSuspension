# Motorcycle Suspension Kinematics Analyzer

Herramienta de análisis de cinemática de suspensiones para equipos de competición de motociclismo.

## Descripción

Este programa permite analizar y visualizar el comportamiento cinemático de suspensiones de motocicletas. Calcula leverage ratios, curvas de progresividad y proporciona visualizaciones interactivas de la geometría.

## Características

- Introducción de geometría de suspensión mediante parámetros configurables
- Cálculo de leverage ratio (motion ratio) a lo largo del recorrido
- Análisis de progresividad (sistemas progresivos, lineales o regresivos)
- Visualización estática de la geometría
- Animación del movimiento de la suspensión
- Exportación de datos a CSV para análisis adicional

## Instalación

### Windows (Recomendado)

Para usuarios de Windows, usa los scripts automatizados:

1. **Instalar dependencias:** Ejecuta `install.bat` (doble clic o desde terminal)
2. **Ejecutar programa:** Ejecuta `run.bat`
3. **Verificar instalación:** Ejecuta `test.bat`

Ver [README_WINDOWS.md](README_WINDOWS.md) para instrucciones detalladas.

### Linux/Mac

1. Clonar el repositorio
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ver [INSTALLATION.md](INSTALLATION.md) para instrucciones completas.

## Uso

Ejecutar el programa principal:

```bash
python main.py
```

El programa presenta un menú interactivo con las siguientes opciones:

1. Visualizar geometría en posición específica
2. Analizar curva de leverage ratio
3. Animar movimiento de suspensión
4. Calcular leverage ratio en posición específica
5. Exportar datos de análisis
6. Modificar geometría
0. Salir

## Sistema de Coordenadas

- **Origen (0,0)**: Eje de giro del basculante (pivote del chasis)
- **Eje X**: Horizontal positivo hacia adelante
- **Eje Y**: Vertical positivo hacia arriba
- **Unidades**: milímetros (mm)

## Configuraciones Soportadas

### Actual
- Sistema directo (amortiguador anclado a basculante y chasis, sin bieletas)

### Futuro
- Sistemas con bieletas
- Configuraciones progresivas complejas

## Arquitectura

El proyecto está organizado en módulos:

- `src/core/`: Geometría fundamental (puntos, vectores, enlaces)
- `src/suspension/`: Sistemas de suspensión
- `src/analysis/`: Herramientas de análisis cinemático
- `src/visualization/`: Visualización y animación
- `examples/`: Configuraciones predefinidas

## Dependencias

- Python >= 3.7
- NumPy >= 1.21.0
- Matplotlib >= 3.5.0
- SciPy >= 1.7.0

## Autores

Equipo de competición motorstudent

## Licencia

Proyecto interno de competición
