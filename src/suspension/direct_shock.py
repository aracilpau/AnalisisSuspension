"""
Sistema de suspensión con amortiguador directo (sin bieletas).

Este módulo implementa un sistema de suspensión donde el amortiguador
está anclado directamente entre el basculante y el chasis, sin bieletas
o sistemas de progresión adicionales.
"""

from dataclasses import dataclass
from typing import Dict
import numpy as np
from scipy.optimize import fsolve

from ..core.geometry import Point
from .base import SuspensionGeometry, SuspensionSystem


@dataclass
class DirectShockGeometry(SuspensionGeometry):
    """
    Geometría de suspensión con amortiguador directo.

    Sistema de coordenadas:
        - Origen (0,0): Eje de giro del basculante (pivote del chasis)
        - Eje X: Horizontal positivo hacia adelante
        - Eje Y: Vertical positivo hacia arriba
        - Unidades: milímetros (mm)

    Attributes:
        swingarm_pivot: Punto de giro del basculante (normalmente el origen)
        swingarm_length: Longitud del basculante desde pivote a eje de rueda (mm)
        swingarm_initial_angle: Ángulo inicial del basculante en grados
                                (0° = horizontal, positivo hacia arriba)
        shock_swingarm_offset: Posición del anclaje del shock en el basculante
                               (coordenadas LOCALES respecto al basculante horizontal)
        shock_chassis_mount: Posición del anclaje del shock en el chasis
                            (coordenadas GLOBALES, punto fijo)
        wheel_radius: Radio de la rueda en mm (para visualización)
    """
    swingarm_pivot: Point
    swingarm_length: float
    swingarm_initial_angle: float  # grados
    shock_swingarm_offset: Point   # coordenadas locales
    shock_chassis_mount: Point     # coordenadas globales
    wheel_radius: float

    def validate(self):
        """
        Valida que la geometría sea físicamente posible.

        Raises:
            ValueError: Si algún parámetro no es válido
        """
        if self.swingarm_length <= 0:
            raise ValueError("La longitud del basculante debe ser positiva")
        if self.wheel_radius <= 0:
            raise ValueError("El radio de rueda debe ser positivo")
        if abs(self.swingarm_initial_angle) > 45:
            print(f"Advertencia: Ángulo de basculante inusualmente alto: {self.swingarm_initial_angle}°")


class DirectShockSuspension(SuspensionSystem):
    """
    Sistema de suspensión con amortiguador directo.

    Implementa todos los cálculos cinemáticos para un sistema donde
    el amortiguador está anclado directamente entre basculante y chasis.
    """

    def __init__(self, geometry: DirectShockGeometry):
        """
        Inicializa el sistema de suspensión.

        Args:
            geometry: Geometría del sistema directo
        """
        super().__init__(geometry)
        geometry.validate()
        self.initial_shock_length = self._calculate_initial_shock_length()

    def _calculate_initial_shock_length(self) -> float:
        """
        Calcula la longitud inicial del amortiguador en posición de reposo.

        Returns:
            Longitud del shock en mm
        """
        initial_angle = np.radians(self.geometry.swingarm_initial_angle)
        shock_mount_swingarm = self._get_shock_swingarm_position(initial_angle)
        return shock_mount_swingarm.distance_to(self.geometry.shock_chassis_mount)

    def _get_shock_swingarm_position(self, swingarm_angle: float) -> Point:
        """
        Calcula la posición global del anclaje del shock en el basculante
        dado el ángulo actual del basculante.

        Rota el offset local del shock según el ángulo del basculante y
        lo transforma a coordenadas globales.

        Args:
            swingarm_angle: Ángulo del basculante en radianes

        Returns:
            Posición global del anclaje del shock en el basculante
        """
        # El offset está definido en coordenadas locales del basculante
        # (como si el basculante estuviera horizontal)
        # Necesitamos rotarlo según el ángulo actual del basculante
        return self.geometry.shock_swingarm_offset.rotate_around(
            Point(0, 0),  # Rotar alrededor del origen local
            swingarm_angle
        )

    def _get_wheel_position(self, swingarm_angle: float) -> Point:
        """
        Calcula la posición del eje de la rueda dado el ángulo del basculante.

        Args:
            swingarm_angle: Ángulo del basculante en radianes

        Returns:
            Posición global del eje de la rueda
        """
        # La rueda está al final del basculante
        wheel_x = self.geometry.swingarm_pivot.x + self.geometry.swingarm_length * np.cos(swingarm_angle)
        wheel_y = self.geometry.swingarm_pivot.y + self.geometry.swingarm_length * np.sin(swingarm_angle)
        return Point(wheel_x, wheel_y)

    def _angle_from_wheel_displacement(self, wheel_displacement: float) -> float:
        """
        Calcula el ángulo del basculante necesario para lograr un
        desplazamiento vertical específico de la rueda.

        Este es un problema de cinemática inversa: dada la posición Y deseada
        de la rueda, encontrar el ángulo del basculante que la produce.

        Usa un solver numérico (scipy.optimize.fsolve) para resolver la ecuación:
            wheel_position(angle).y = initial_wheel_y + wheel_displacement

        Args:
            wheel_displacement: Desplazamiento vertical deseado en mm
                              (positivo = hacia arriba / compresión)

        Returns:
            Ángulo del basculante en radianes
        """
        # Posición inicial
        initial_angle = np.radians(self.geometry.swingarm_initial_angle)
        initial_wheel_pos = self._get_wheel_position(initial_angle)
        target_y = initial_wheel_pos.y + wheel_displacement

        def equation(angle):
            """Ecuación a resolver: posición Y actual - posición Y deseada = 0"""
            wheel_pos = self._get_wheel_position(angle[0])
            return wheel_pos.y - target_y

        # Resolver usando el ángulo inicial como punto de partida
        solution = fsolve(equation, [initial_angle])
        return solution[0]

    def calculate_shock_position(self, wheel_displacement: float) -> Point:
        """
        Calcula la posición del anclaje del amortiguador en el basculante
        dado un desplazamiento vertical de la rueda.

        Args:
            wheel_displacement: Desplazamiento vertical de la rueda en mm
                              (positivo = compresión hacia arriba)

        Returns:
            Posición del anclaje del shock en el basculante
        """
        angle = self._angle_from_wheel_displacement(wheel_displacement)
        return self._get_shock_swingarm_position(angle)

    def calculate_leverage_ratio(self, wheel_displacement: float) -> float:
        """
        Calcula el leverage ratio (motion ratio) en una posición específica.

        El leverage ratio se calcula mediante diferenciación numérica:
            LR = d(wheel_travel) / d(shock_travel)

        Se usa un delta pequeño (0.1 mm) para aproximar la derivada.

        Args:
            wheel_displacement: Desplazamiento vertical de la rueda en mm

        Returns:
            Leverage ratio (adimensional)
        """
        delta = 0.1  # mm - incremento pequeño para derivada numérica

        # Posición actual
        shock_pos_current = self.calculate_shock_position(wheel_displacement)
        shock_length_current = shock_pos_current.distance_to(
            self.geometry.shock_chassis_mount
        )

        # Posición con incremento
        shock_pos_next = self.calculate_shock_position(wheel_displacement + delta)
        shock_length_next = shock_pos_next.distance_to(
            self.geometry.shock_chassis_mount
        )

        # Cambio en longitud del shock
        delta_shock = shock_length_next - shock_length_current

        # Leverage ratio
        if abs(delta_shock) < 1e-10:
            # Singularidad: el shock no se mueve
            return float('inf')

        return delta / delta_shock

    def get_all_points(self, wheel_displacement: float) -> Dict[str, Point]:
        """
        Retorna todas las posiciones de puntos clave para visualización.

        Args:
            wheel_displacement: Desplazamiento vertical de la rueda en mm

        Returns:
            Diccionario con puntos clave:
                - 'swingarm_pivot': Pivote del basculante
                - 'wheel_axle': Eje de la rueda
                - 'shock_swingarm': Anclaje del shock en basculante
                - 'shock_chassis': Anclaje del shock en chasis (fijo)
        """
        angle = self._angle_from_wheel_displacement(wheel_displacement)

        return {
            'swingarm_pivot': self.geometry.swingarm_pivot,
            'wheel_axle': self._get_wheel_position(angle),
            'shock_swingarm': self._get_shock_swingarm_position(angle),
            'shock_chassis': self.geometry.shock_chassis_mount,
        }

    def _get_shock_chassis_mount(self) -> Point:
        """
        Retorna el punto de anclaje fijo del shock en el chasis.

        Returns:
            Punto de anclaje del shock en el chasis
        """
        return self.geometry.shock_chassis_mount

    def get_swingarm_angle(self, wheel_displacement: float) -> float:
        """
        Obtiene el ángulo del basculante para un desplazamiento de rueda dado.

        Args:
            wheel_displacement: Desplazamiento vertical de la rueda en mm

        Returns:
            Ángulo del basculante en grados
        """
        angle_rad = self._angle_from_wheel_displacement(wheel_displacement)
        return np.degrees(angle_rad)

    def validate_geometry(self) -> bool:
        """
        Valida que la geometría sea físicamente posible.

        Verifica que el shock pueda alcanzar entre los anclajes y que
        no haya configuraciones imposibles.

        Returns:
            True si la geometría es válida

        Raises:
            ValueError: Si la geometría no es válida
        """
        # Validación básica
        self.geometry.validate()

        # Verificar que el shock pueda alcanzar entre anclajes
        initial_shock_length = self.initial_shock_length

        # Simular un rango de movimiento y verificar que sea razonable
        try:
            test_range = [-30, 0, 30]  # mm
            for disp in test_range:
                lr = self.calculate_leverage_ratio(disp)
                if lr < 0.5 or lr > 10.0:
                    print(f"Advertencia: Leverage ratio inusual ({lr:.2f}) en desplazamiento {disp} mm")
        except Exception as e:
            raise ValueError(f"Error validando geometría: {e}")

        return True

    def __repr__(self) -> str:
        return (
            f"DirectShockSuspension(\n"
            f"  swingarm_length={self.geometry.swingarm_length:.1f} mm,\n"
            f"  initial_angle={self.geometry.swingarm_initial_angle:.1f}°,\n"
            f"  initial_shock_length={self.initial_shock_length:.1f} mm\n"
            f")"
        )
