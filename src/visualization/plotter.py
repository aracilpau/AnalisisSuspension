"""
Visualización estática de geometría de suspensión.

Este módulo proporciona herramientas para crear gráficos estáticos
de la geometría de suspensión y curvas de análisis usando matplotlib.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from typing import Dict, Tuple

from ..suspension.base import SuspensionSystem
from ..core.geometry import Point


class SuspensionPlotter:
    """
    Clase para visualización estática de suspensiones.

    Attributes:
        suspension: Sistema de suspensión a visualizar
        figsize: Tamaño de las figuras (ancho, alto) en pulgadas
    """

    def __init__(self, suspension: SuspensionSystem, figsize: Tuple[int, int] = (15, 10)):
        """
        Inicializa el plotter.

        Args:
            suspension: Sistema de suspensión a visualizar
            figsize: Tamaño de las figuras (ancho, alto) en pulgadas
        """
        self.suspension = suspension
        self.figsize = figsize

    def plot_geometry(
        self,
        wheel_displacement: float = 0,
        show_grid: bool = True,
        show_dimensions: bool = True
    ) -> Tuple:
        """
        Dibuja la geometría de la suspensión en una posición específica.

        Args:
            wheel_displacement: Desplazamiento de rueda en mm
            show_grid: Si mostrar la cuadrícula
            show_dimensions: Si mostrar dimensiones y ángulos

        Returns:
            Tupla (fig, ax) con la figura y ejes de matplotlib
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        # Obtener todos los puntos
        points = self.suspension.get_all_points(wheel_displacement)

        # Dibujar componentes
        self._draw_swingarm(ax, points)
        self._draw_shock(ax, points)
        self._draw_wheel(ax, points)
        self._draw_ground_reference(ax, points)

        # Marcar puntos clave
        self._draw_key_points(ax, points)

        # Mostrar dimensiones si se solicita
        if show_dimensions:
            self._draw_dimensions(ax, points, wheel_displacement)

        # Configurar ejes
        ax.set_aspect('equal')
        if show_grid:
            ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xlabel('X (mm)', fontsize=12)
        ax.set_ylabel('Y (mm)', fontsize=12)

        # Título
        lr = self.suspension.calculate_leverage_ratio(wheel_displacement)
        title = f'Geometría de Suspensión\n'
        title += f'Desplazamiento Rueda: {wheel_displacement:.1f} mm | '
        title += f'Leverage Ratio: {lr:.3f}'
        ax.set_title(title, fontsize=14, fontweight='bold')

        # Ajustar límites para ver toda la geometría
        self._auto_scale_axes(ax, points)

        # Leyenda
        ax.legend(loc='upper right', fontsize=10)

        plt.tight_layout()
        return fig, ax

    def plot_leverage_curve(self, analysis_results: Dict) -> Tuple:
        """
        Dibuja las curvas de leverage ratio y desplazamientos.

        Args:
            analysis_results: Resultados del análisis de LeverageAnalyzer

        Returns:
            Tupla (fig, (ax1, ax2)) con figura y ejes
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.figsize)

        wheel_travel = analysis_results['wheel_travel']
        leverage_ratio = analysis_results['leverage_ratio']
        shock_travel = analysis_results['shock_travel']

        # Gráfico 1: Leverage Ratio vs Wheel Travel
        ax1.plot(wheel_travel, leverage_ratio, 'b-', linewidth=2.5, label='Leverage Ratio')
        ax1.axhline(
            y=analysis_results['lr_initial'],
            color='r',
            linestyle='--',
            linewidth=1.5,
            label=f'LR Inicial: {analysis_results["lr_initial"]:.3f}'
        )
        ax1.axvline(x=0, color='gray', linestyle=':', linewidth=1, alpha=0.7)
        ax1.grid(True, alpha=0.3)
        ax1.set_xlabel('Desplazamiento Rueda (mm)', fontsize=11)
        ax1.set_ylabel('Leverage Ratio', fontsize=11)

        # Título con información de progresividad
        title1 = f'Curva de Leverage Ratio - Sistema {analysis_results["system_type"].upper()}\n'
        title1 += f'Progresividad: {analysis_results["progression_percent"]:.1f}% | '
        title1 += f'LR Promedio: {analysis_results["lr_average"]:.3f} | '
        title1 += f'Rango: {analysis_results["lr_min"]:.3f} - {analysis_results["lr_max"]:.3f}'
        ax1.set_title(title1, fontsize=12, fontweight='bold')
        ax1.legend(fontsize=10)

        # Gráfico 2: Wheel Travel vs Shock Travel
        ax2.plot(shock_travel, wheel_travel, 'g-', linewidth=2.5, label='Curva de Movimiento')
        ax2.axhline(y=0, color='gray', linestyle=':', linewidth=1, alpha=0.7)
        ax2.axvline(x=0, color='gray', linestyle=':', linewidth=1, alpha=0.7)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlabel('Desplazamiento Shock (mm)', fontsize=11)
        ax2.set_ylabel('Desplazamiento Rueda (mm)', fontsize=11)
        ax2.set_title('Relación Desplazamiento Rueda vs Shock', fontsize=12, fontweight='bold')
        ax2.legend(fontsize=10)

        # Añadir línea de referencia lineal (LR constante)
        if len(shock_travel) > 0 and len(wheel_travel) > 0:
            # Calcular pendiente promedio
            valid_mask = ~(np.isnan(shock_travel) | np.isnan(wheel_travel))
            if np.sum(valid_mask) > 1:
                slope = np.nanmean(leverage_ratio)
                shock_range = np.array([np.nanmin(shock_travel), np.nanmax(shock_travel)])
                wheel_reference = shock_range * slope
                ax2.plot(
                    shock_range,
                    wheel_reference,
                    'r--',
                    linewidth=1.5,
                    alpha=0.6,
                    label=f'Referencia Lineal (LR={slope:.2f})'
                )
                ax2.legend(fontsize=10)

        plt.tight_layout()
        return fig, (ax1, ax2)

    def _draw_swingarm(self, ax, points: Dict):
        """Dibuja el basculante."""
        pivot = points['swingarm_pivot']
        wheel = points['wheel_axle']

        ax.plot(
            [pivot.x, wheel.x],
            [pivot.y, wheel.y],
            'ko-',
            linewidth=4,
            markersize=10,
            label='Basculante',
            zorder=3
        )

    def _draw_shock(self, ax, points: Dict):
        """Dibuja el amortiguador."""
        shock_sw = points['shock_swingarm']
        shock_ch = points['shock_chassis']

        # Calcular longitud del shock
        length = shock_sw.distance_to(shock_ch)

        ax.plot(
            [shock_sw.x, shock_ch.x],
            [shock_sw.y, shock_ch.y],
            'ro-',
            linewidth=3,
            markersize=8,
            label=f'Amortiguador ({length:.1f} mm)',
            zorder=4
        )

    def _draw_wheel(self, ax, points: Dict):
        """Dibuja la rueda."""
        wheel = points['wheel_axle']
        radius = self.suspension.geometry.wheel_radius

        # Círculo de la rueda
        circle = Circle(
            (wheel.x, wheel.y),
            radius,
            fill=False,
            edgecolor='blue',
            linewidth=2.5,
            label='Rueda',
            zorder=2
        )
        ax.add_patch(circle)

        # Marcar el centro
        ax.plot(wheel.x, wheel.y, 'b+', markersize=12, markeredgewidth=2)

    def _draw_ground_reference(self, ax, points: Dict):
        """Dibuja una línea de referencia del suelo."""
        wheel = points['wheel_axle']
        radius = self.suspension.geometry.wheel_radius

        # Línea del suelo
        ground_y = wheel.y - radius
        x_min, x_max = ax.get_xlim()

        ax.axhline(
            y=ground_y,
            color='brown',
            linestyle='-',
            linewidth=2,
            alpha=0.5,
            label='Suelo (ref)'
        )

    def _draw_key_points(self, ax, points: Dict):
        """Marca puntos clave con anotaciones."""
        labels = {
            'swingarm_pivot': 'Pivote',
            'wheel_axle': 'Eje Rueda',
            'shock_swingarm': 'Anclaje SW',
            'shock_chassis': 'Anclaje Chasis'
        }

        for name, point in points.items():
            if name in labels:
                ax.plot(point.x, point.y, 'ko', markersize=6, zorder=5)
                ax.annotate(
                    labels[name],
                    (point.x, point.y),
                    xytext=(8, 8),
                    textcoords='offset points',
                    fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                    zorder=6
                )

    def _draw_dimensions(self, ax, points: Dict, wheel_displacement: float):
        """Dibuja dimensiones y ángulos clave."""
        # Longitud del shock
        shock_sw = points['shock_swingarm']
        shock_ch = points['shock_chassis']
        shock_length = shock_sw.distance_to(shock_ch)

        # Añadir texto con información
        info_text = f'Longitud Shock: {shock_length:.1f} mm\n'
        info_text += f'Despl. Shock: {shock_length - self.suspension.initial_shock_length:.1f} mm'

        ax.text(
            0.02, 0.98,
            info_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )

    def _auto_scale_axes(self, ax, points: Dict):
        """Ajusta automáticamente los límites de los ejes."""
        # Extraer todas las coordenadas
        all_x = [p.x for p in points.values()]
        all_y = [p.y for p in points.values()]

        # Añadir margen del radio de rueda
        radius = self.suspension.geometry.wheel_radius
        all_y.append(points['wheel_axle'].y - radius)

        # Calcular límites con margen
        margin_x = (max(all_x) - min(all_x)) * 0.15
        margin_y = (max(all_y) - min(all_y)) * 0.15

        ax.set_xlim(min(all_x) - margin_x, max(all_x) + margin_x)
        ax.set_ylim(min(all_y) - margin_y, max(all_y) + margin_y)

    def plot_comparison(
        self,
        positions: list,
        labels: list = None
    ) -> Tuple:
        """
        Dibuja múltiples posiciones de la suspensión en la misma figura.

        Args:
            positions: Lista de desplazamientos de rueda a comparar
            labels: Etiquetas para cada posición (opcional)

        Returns:
            Tupla (fig, ax) con figura y ejes
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        colors = plt.cm.viridis(np.linspace(0, 1, len(positions)))

        if labels is None:
            labels = [f'{pos:.0f} mm' for pos in positions]

        # Dibujar cada posición
        for i, (pos, color, label) in enumerate(zip(positions, colors, labels)):
            points = self.suspension.get_all_points(pos)

            # Basculante
            pivot = points['swingarm_pivot']
            wheel = points['wheel_axle']
            ax.plot(
                [pivot.x, wheel.x],
                [pivot.y, wheel.y],
                'o-',
                color=color,
                linewidth=2,
                markersize=6,
                label=f'Basculante {label}',
                alpha=0.7
            )

            # Shock
            shock_sw = points['shock_swingarm']
            shock_ch = points['shock_chassis']
            ax.plot(
                [shock_sw.x, shock_ch.x],
                [shock_sw.y, shock_ch.y],
                's-',
                color=color,
                linewidth=2,
                markersize=5,
                alpha=0.7
            )

        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('X (mm)', fontsize=12)
        ax.set_ylabel('Y (mm)', fontsize=12)
        ax.set_title('Comparación de Posiciones', fontsize=14, fontweight='bold')
        ax.legend(fontsize=9)

        plt.tight_layout()
        return fig, ax
