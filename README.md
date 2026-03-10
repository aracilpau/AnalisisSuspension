# ISC - Ingenieria de Suspension para Competicion

Plataforma web de ingenieria de suspension para el equipo de MotoStudent. Herramientas de calculo y analisis para disenar y ajustar la suspension de la moto de competicion.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey?logo=flask)
![License](https://img.shields.io/badge/License-MIT-green)

## Estudios disponibles

| Estudio | Descripcion |
|---------|-------------|
| **Analisis de Suspension** | Leverage ratio, visualizacion de geometria, animacion y exportacion CSV |
| **Calculadora de Sag** | Sag estatico trasero con equilibrio de fuerzas y leverage ratio |
| **Horquilla Delantera** | Sag delantero, comparacion de muelles para Ohlins FGAM027 |
| **Conceptos** | Glosario completo: muelle, amortiguador, precarga, progresividad... |

## Demo

La app esta desplegada en Render: **https://analisissuspension.onrender.com**

## Ejecutar en local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Lanzar servidor de desarrollo
python web_app.py
```

Abrir http://localhost:5000 en el navegador.

## Stack

- **Backend**: Python, Flask, NumPy, SciPy, Matplotlib
- **Frontend**: HTML/CSS/JS vanilla (dark theme, 6 paletas)
- **Deploy**: Gunicorn + Render

## Arquitectura

```
web_app.py                 # Flask API (endpoints REST)
web/
  templates/index.html     # SPA - toda la UI
  static/
    css/style.css          # Dark theme con variables CSS
    js/app.js              # Logica de navegacion y fetch
src/
  core/geometry.py         # Primitivas: Point, Vector2D, Link
  suspension/
    base.py                # Clases abstractas
    direct_shock.py        # Implementacion sistema directo
  analysis/
    leverage_ratio.py      # Analisis de leverage ratio
  visualization/
    plotter.py             # Graficos matplotlib
    animator.py            # Animaciones GIF
examples/
  sample_configs.py        # 5 presets de geometria (Sportbike, Enduro, MotoGP...)
```

## Componentes de la moto

- **Amortiguador trasero**: Ohlins S36DR1 (278mm libre, 59mm stroke)
- **Horquilla delantera**: Ohlins FGAM027 (110mm recorrido, muelles 35-65 N/mm)

## Equipo

Proyecto del equipo de MotoStudent - ISC Racing
