"""
Animación de movimiento de suspensión.

Este módulo proporciona herramientas para crear animaciones del
movimiento de suspensiones usando matplotlib.animation.
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import numpy as np
from typing import Tuple

from ..suspension.base import SuspensionSystem
from .plotter import SuspensionPlotter


class SuspensionAnimator:
    """
    Crea animaciones del movimiento de suspensión.

    Attributes:
        suspension: Sistema de suspensión a animar
        plotter: SuspensionPlotter para renderizado
    """

    def __init__(self, suspension: SuspensionSystem, plotter: SuspensionPlotter = None):
        """
        Inicializa el animador.

        Args:
            suspension: Sistema de suspensión a animar
            plotter: SuspensionPlotter opcional (se crea uno si no se proporciona)
        """
        self.suspension = suspension
        self.plotter = plotter if plotter is not None else SuspensionPlotter(suspension)

    def animate_travel(
        self,
        travel_range: Tuple[float, float] = (-50, 50),
        num_frames: int = 100,
        interval: int = 50,
        repeat: bool = True,
        show_trail: bool = False
    ) -> FuncAnimation:
        """
        Crea una animación del movimiento completo de la suspensión.

        Args:
            travel_range: Tupla (min, max) desplazamiento de rueda en mm
            num_frames: Número de frames en la animación
            interval: Milisegundos entre frames
            repeat: Si la animación debe repetirse
            show_trail: Si mostrar rastro del movimiento

        Returns:
            Objeto FuncAnimation de matplotlib
        """
        fig, ax = plt.subplots(figsize=self.plotter.figsize)

        # Generar posiciones para cada frame
        travel_min, travel_max = travel_range
        wheel_positions = np.linspace(travel_min, travel_max, num_frames)

        # Pre-calcular límites de los ejes para mantenerlos fijos
        all_points_for_limits = []
        for pos in [travel_min, 0, travel_max]:
            points = self.suspension.get_all_points(pos)
            all_points_for_limits.extend(points.values())

        all_x = [p.x for p in all_points_for_limits]
        all_y = [p.y for p in all_points_for_limits]
        radius = self.suspension.geometry.wheel_radius
        all_y.append(min(all_y) - radius)

        margin_x = (max(all_x) - min(all_x)) * 0.15
        margin_y = (max(all_y) - min(all_y)) * 0.15

        xlim = (min(all_x) - margin_x, max(all_x) + margin_x)
        ylim = (min(all_y) - margin_y, max(all_y) + margin_y)

        # Elementos que se actualizarán
        swingarm_line, = ax.plot([], [], 'ko-', linewidth=4, markersize=10, label='Basculante')
        shock_line, = ax.plot([], [], 'ro-', linewidth=3, markersize=8, label='Amortiguador')
        wheel_circle = Circle((0, 0), radius, fill=False, edgecolor='blue', linewidth=2.5)
        ax.add_patch(wheel_circle)

        # Línea del suelo
        ground_line = ax.axhline(y=0, color='brown', linestyle='-', linewidth=2, alpha=0.5, label='Suelo')

        # Elementos para trail (si se solicita)
        trail_lines = []
        if show_trail:
            shock_trail, = ax.plot([], [], 'r.', markersize=2, alpha=0.3)
            wheel_trail, = ax.plot([], [], 'b.', markersize=2, alpha=0.3)
            trail_lines = [shock_trail, wheel_trail]

        # Texto informativo
        info_text = ax.text(
            0.02, 0.98, '',
            transform=ax.transAxes,
            fontsize=11,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9),
            family='monospace'
        )

        # Listas para almacenar posiciones del trail
        shock_trail_x = []
        shock_trail_y = []
        wheel_trail_x = []
        wheel_trail_y = []

        def init():
            """Inicializa la animación."""
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_xlabel('X (mm)', fontsize=12)
            ax.set_ylabel('Y (mm)', fontsize=12)
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
            ax.legend(loc='upper right', fontsize=10)

            return [swingarm_line, shock_line, wheel_circle, ground_line, info_text] + trail_lines

        def update(frame):
            """Actualiza cada frame de la animación."""
            wheel_disp = wheel_positions[frame]
            points = self.suspension.get_all_points(wheel_disp)

            # Actualizar basculante
            pivot = points['swingarm_pivot']
            wheel = points['wheel_axle']
            swingarm_line.set_data([pivot.x, wheel.x], [pivot.y, wheel.y])

            # Actualizar amortiguador
            shock_sw = points['shock_swingarm']
            shock_ch = points['shock_chassis']
            shock_line.set_data([shock_sw.x, shock_ch.x], [shock_sw.y, shock_ch.y])

            # Actualizar rueda
            wheel_circle.center = (wheel.x, wheel.y)

            # Actualizar línea del suelo
            ground_y = wheel.y - radius
            ground_line.set_ydata([ground_y, ground_y])

            # Actualizar trail si está habilitado
            if show_trail:
                shock_trail_x.append(shock_sw.x)
                shock_trail_y.append(shock_sw.y)
                wheel_trail_x.append(wheel.x)
                wheel_trail_y.append(wheel.y)

                # Limitar longitud del trail
                max_trail_length = 50
                if len(shock_trail_x) > max_trail_length:
                    shock_trail_x.pop(0)
                    shock_trail_y.pop(0)
                    wheel_trail_x.pop(0)
                    wheel_trail_y.pop(0)

                trail_lines[0].set_data(shock_trail_x, shock_trail_y)
                trail_lines[1].set_data(wheel_trail_x, wheel_trail_y)

            # Calcular info
            lr = self.suspension.calculate_leverage_ratio(wheel_disp)
            shock_length = shock_sw.distance_to(shock_ch)
            shock_travel = shock_length - self.suspension.initial_shock_length

            # Actualizar texto informativo
            info = f'Frame: {frame + 1}/{num_frames}\n'
            info += f'Rueda:     {wheel_disp:+7.1f} mm\n'
            info += f'Shock:     {shock_travel:+7.1f} mm\n'
            info += f'LR:        {lr:7.3f}\n'
            info += f'Shock Len: {shock_length:7.1f} mm'
            info_text.set_text(info)

            # Actualizar título
            ax.set_title(
                f'Animación de Suspensión - Desplazamiento: {wheel_disp:+.1f} mm',
                fontsize=14,
                fontweight='bold'
            )

            return [swingarm_line, shock_line, wheel_circle, ground_line, info_text] + trail_lines

        anim = FuncAnimation(
            fig,
            update,
            frames=num_frames,
            init_func=init,
            interval=interval,
            blit=True,
            repeat=repeat
        )

        return anim

    def animate_compression_rebound(
        self,
        max_travel: float = 50,
        num_frames: int = 60,
        interval: int = 50
    ) -> FuncAnimation:
        """
        Crea una animación de compresión seguida de rebote (ciclo completo).

        Args:
            max_travel: Máximo desplazamiento en mm
            num_frames: Frames por dirección (total = 2 * num_frames)
            interval: Milisegundos entre frames

        Returns:
            Objeto FuncAnimation
        """
        # Crear secuencia: 0 -> max -> 0 -> -max -> 0
        compression = np.linspace(0, max_travel, num_frames)
        rebound = np.linspace(max_travel, -max_travel, 2 * num_frames)
        extension = np.linspace(-max_travel, 0, num_frames)

        full_sequence = np.concatenate([compression, rebound, extension])

        return self.animate_travel(
            travel_range=(min(full_sequence), max(full_sequence)),
            num_frames=len(full_sequence),
            interval=interval,
            repeat=True,
            show_trail=True
        )

    def save_animation(
        self,
        filename: str,
        travel_range: Tuple[float, float] = (-50, 50),
        num_frames: int = 100,
        fps: int = 20,
        dpi: int = 100
    ):
        """
        Guarda la animación como archivo de video.

        Requiere ffmpeg instalado en el sistema.

        Args:
            filename: Nombre del archivo de salida (con extensión .mp4, .gif, etc.)
            travel_range: Rango de desplazamiento
            num_frames: Número de frames
            fps: Frames por segundo
            dpi: Resolución en DPI

        Raises:
            RuntimeError: Si ffmpeg no está disponible
        """
        anim = self.animate_travel(
            travel_range=travel_range,
            num_frames=num_frames,
            interval=1000//fps,
            repeat=False
        )

        try:
            if filename.endswith('.gif'):
                anim.save(filename, writer='pillow', fps=fps, dpi=dpi)
            else:
                anim.save(filename, writer='ffmpeg', fps=fps, dpi=dpi)
            print(f"Animación guardada en: {filename}")
        except Exception as e:
            raise RuntimeError(f"Error guardando animación: {e}")

    def create_side_by_side_comparison(
        self,
        suspension2: SuspensionSystem,
        travel_range: Tuple[float, float] = (-50, 50),
        num_frames: int = 100,
        interval: int = 50,
        labels: Tuple[str, str] = ('Configuración 1', 'Configuración 2')
    ) -> FuncAnimation:
        """
        Crea animación comparando dos configuraciones lado a lado.

        Args:
            suspension2: Segunda suspensión a comparar
            travel_range: Rango de desplazamiento
            num_frames: Número de frames
            interval: Milisegundos entre frames
            labels: Etiquetas para cada configuración

        Returns:
            Objeto FuncAnimation
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

        # Generar posiciones
        travel_min, travel_max = travel_range
        wheel_positions = np.linspace(travel_min, travel_max, num_frames)

        # Configurar ambos axes de manera similar
        for ax, suspension, label in [(ax1, self.suspension, labels[0]),
                                      (ax2, suspension2, labels[1])]:
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_xlabel('X (mm)', fontsize=11)
            ax.set_ylabel('Y (mm)', fontsize=11)
            ax.set_title(label, fontsize=13, fontweight='bold')

        # Elementos animados para cada suspensión
        elements1 = self._create_animated_elements(ax1, self.suspension)
        elements2 = self._create_animated_elements(ax2, suspension2)

        def update(frame):
            wheel_disp = wheel_positions[frame]

            # Actualizar primera suspensión
            self._update_elements(elements1, self.suspension, wheel_disp, ax1)

            # Actualizar segunda suspensión
            self._update_elements(elements2, suspension2, wheel_disp, ax2)

            return elements1['all'] + elements2['all']

        anim = FuncAnimation(
            fig,
            update,
            frames=num_frames,
            interval=interval,
            blit=True,
            repeat=True
        )

        plt.tight_layout()
        return anim

    def _create_animated_elements(self, ax, suspension):
        """Crea elementos animados para un eje."""
        radius = suspension.geometry.wheel_radius

        swingarm_line, = ax.plot([], [], 'ko-', linewidth=3, markersize=8)
        shock_line, = ax.plot([], [], 'ro-', linewidth=2.5, markersize=6)
        wheel_circle = Circle((0, 0), radius, fill=False, edgecolor='blue', linewidth=2)
        ax.add_patch(wheel_circle)

        info_text = ax.text(
            0.02, 0.98, '',
            transform=ax.transAxes,
            fontsize=9,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
            family='monospace'
        )

        return {
            'swingarm': swingarm_line,
            'shock': shock_line,
            'wheel': wheel_circle,
            'info': info_text,
            'all': [swingarm_line, shock_line, wheel_circle, info_text]
        }

    def _update_elements(self, elements, suspension, wheel_disp, ax):
        """Actualiza elementos animados."""
        points = suspension.get_all_points(wheel_disp)

        # Basculante
        pivot = points['swingarm_pivot']
        wheel = points['wheel_axle']
        elements['swingarm'].set_data([pivot.x, wheel.x], [pivot.y, wheel.y])

        # Shock
        shock_sw = points['shock_swingarm']
        shock_ch = points['shock_chassis']
        elements['shock'].set_data([shock_sw.x, shock_ch.x], [shock_sw.y, shock_ch.y])

        # Rueda
        elements['wheel'].center = (wheel.x, wheel.y)

        # Info
        lr = suspension.calculate_leverage_ratio(wheel_disp)
        info = f'Rueda: {wheel_disp:+.1f} mm\nLR: {lr:.3f}'
        elements['info'].set_text(info)

        # Auto-escalar ejes si es necesario
        ax.relim()
        ax.autoscale_view()
