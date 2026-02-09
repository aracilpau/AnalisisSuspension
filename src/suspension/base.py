"""
Clases base abstractas para sistemas de suspensión.

Este módulo define la interfaz común que deben implementar todos
los sistemas de suspensión (directo, con bieletas, etc.).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict
import numpy as np

from ..core.geometry import Point


@dataclass
class SuspensionGeometry:
    """
    Clase base para datos de geometría de suspensión.

    Las subclases deben definir los campos específicos para cada tipo
    de sistema de suspensión.
    """
    pass


class SuspensionSystem(ABC):
    """
    Clase abstracta base para todos los sistemas de suspensión.

    Define la interfaz común que todos los sistemas deben implementar,
    permitiendo análisis y visualización consistentes independientemente
    del tipo de suspensión.

    Attributes:
        geometry (SuspensionGeometry): Geometría del sistema
        initial_shock_length (float): Longitud inicial del amortiguador en mm
    """

    def __init__(self, geometry: SuspensionGeometry):
        """
        Inicializa el sistema de suspensión.

        Args:
            geometry: Geometría del sistema de suspensión
        """
        self.geometry = geometry
        self.initial_shock_length = None  # Se calcula en subclases

    @abstractmethod
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
        pass

    @abstractmethod
    def calculate_leverage_ratio(self, wheel_displacement: float) -> float:
        """
        Calcula el leverage ratio (motion ratio) en una posición específica.

        El leverage ratio se define como:
            LR = d(wheel_travel) / d(shock_travel)

        Un LR más alto significa que el amortiguador se mueve menos que la rueda,
        resultando en una suspensión más "suave" para la misma rigidez de muelle.

        Args:
            wheel_displacement: Desplazamiento vertical de la rueda en mm

        Returns:
            Leverage ratio (adimensional)
        """
        pass

    @abstractmethod
    def get_all_points(self, wheel_displacement: float) -> Dict[str, Point]:
        """
        Retorna todas las posiciones de puntos clave para visualización.

        Los puntos exactos dependen del tipo de suspensión, pero típicamente
        incluyen: pivote del basculante, eje de rueda, anclajes del shock, etc.

        Args:
            wheel_displacement: Desplazamiento vertical de la rueda en mm

        Returns:
            Diccionario {nombre_punto: Point} con todos los puntos clave
        """
        pass

    def calculate_progression_curve(
        self,
        travel_range: tuple = (-50, 50),
        num_points: int = 100
    ) -> tuple:
        """
        Calcula la curva completa de progresividad a lo largo del recorrido.

        Args:
            travel_range: Tupla (min, max) de desplazamiento de rueda en mm
            num_points: Número de puntos a calcular

        Returns:
            Tupla (wheel_displacements, leverage_ratios, shock_displacements)
            - wheel_displacements: Array de desplazamientos de rueda
            - leverage_ratios: Array de leverage ratios
            - shock_displacements: Array de desplazamientos de shock
        """
        travel_min, travel_max = travel_range
        wheel_displacements = np.linspace(travel_min, travel_max, num_points)
        leverage_ratios = np.zeros(num_points)
        shock_displacements = np.zeros(num_points)

        for i, wheel_disp in enumerate(wheel_displacements):
            try:
                leverage_ratios[i] = self.calculate_leverage_ratio(wheel_disp)
                shock_pos = self.calculate_shock_position(wheel_disp)
                shock_displacements[i] = self._calculate_shock_displacement(shock_pos)
            except Exception as e:
                # Si hay error en algún punto, usar NaN
                leverage_ratios[i] = np.nan
                shock_displacements[i] = np.nan

        return wheel_displacements, leverage_ratios, shock_displacements

    def _calculate_shock_displacement(self, shock_pos: Point) -> float:
        """
        Calcula el desplazamiento del shock respecto a su posición inicial.

        Este es un método auxiliar interno que debe funcionar para cualquier
        tipo de suspensión.

        Args:
            shock_pos: Posición actual del anclaje del shock en el basculante

        Returns:
            Desplazamiento del shock en mm (positivo = compresión)
        """
        if self.initial_shock_length is None:
            raise ValueError("initial_shock_length no está inicializado")

        # Necesitamos acceder al anclaje fijo del shock
        # Las subclases deben proporcionar esto en su geometría
        current_length = shock_pos.distance_to(self._get_shock_chassis_mount())
        return current_length - self.initial_shock_length

    @abstractmethod
    def _get_shock_chassis_mount(self) -> Point:
        """
        Retorna el punto de anclaje fijo del shock en el chasis.

        Este método auxiliar permite a la clase base calcular desplazamientos
        del shock sin conocer los detalles específicos de cada geometría.

        Returns:
            Punto de anclaje del shock en el chasis
        """
        pass

    def validate_geometry(self) -> bool:
        """
        Valida que la geometría sea físicamente posible.

        Las subclases pueden sobrescribir este método para añadir
        validaciones específicas.

        Returns:
            True si la geometría es válida

        Raises:
            ValueError: Si la geometría no es válida
        """
        return True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(geometry={self.geometry})"
