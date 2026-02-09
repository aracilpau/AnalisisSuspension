# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Motorcycle Suspension Kinematics Analyzer — a Python tool for analyzing and visualizing motorcycle suspension geometry, leverage ratios (motion ratios), and progressivity. Built for the MotorStudent competition team.

Currently implements **direct shock systems only** (no linkage). The abstract base classes (`SuspensionSystem`, `SuspensionGeometry`) are designed for future linkage system implementations.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the interactive CLI
python main.py

# Run tests
python test_basic.py

# Windows batch helpers
install.bat    # install deps
run.bat        # run main
test.bat       # run tests
```

## Architecture

```
src/
├── core/geometry.py          # Primitives: Point, Vector2D, Link
├── suspension/
│   ├── base.py               # Abstract base: SuspensionSystem, SuspensionGeometry
│   └── direct_shock.py       # DirectShockSuspension implementation
├── analysis/leverage_ratio.py # LeverageAnalyzer: travel analysis, wheel rate, spring optimization
└── visualization/
    ├── plotter.py             # Static matplotlib plots (geometry, leverage curves)
    └── animator.py            # Animated suspension travel visualization
examples/sample_configs.py     # 5 preset geometries (Sportbike, Enduro, Supermoto, Touring, MotoGP)
main.py                        # Interactive menu-driven CLI
```

**Key dependency flow:** `geometry.py` → `suspension/` → `analysis/` and `visualization/`

## Coordinate System & Units

- **Origin:** Swingarm pivot (0, 0)
- **X:** horizontal (positive forward), **Y:** vertical (positive upward)
- **Units:** millimeters (mm)
- **Angles:** degrees in user-facing code, radians internally

## Key Technical Details

- Inverse kinematics solved via `scipy.optimize.fsolve` (wheel displacement → swingarm angle)
- Leverage ratio computed by numerical differentiation with delta = 0.1 mm
- Leverage ratio = Δwheel / Δshock; wheel rate = spring_rate / LR²
- Progressivity classification: >5% progressive, <-5% regressive, else linear
- CSV export format: wheel travel, shock travel, leverage ratio, shock velocity

## Language

Code comments and docstrings are in **Spanish**. Maintain this convention.
