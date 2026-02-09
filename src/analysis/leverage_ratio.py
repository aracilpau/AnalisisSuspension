"""
Análisis de leverage ratio y progresividad de suspensiones.

Este módulo proporciona herramientas para analizar el comportamiento
cinemático de suspensiones a lo largo de todo su recorrido.
"""

import numpy as np
from typing import Dict, Tuple
from ..suspension.base import SuspensionSystem
from ..core.geometry import Point


class LeverageAnalyzer:
    """
    Analizador de leverage ratio y progresividad de suspensiones.

    Attributes:
        suspension: Sistema de suspensión a analizar
    """

    def __init__(self, suspension: SuspensionSystem):
        """
        Inicializa el analizador.

        Args:
            suspension: Sistema de suspensión a analizar
        """
        self.suspension = suspension

    def analyze_travel_range(
        self,
        travel_min: float = -50,
        travel_max: float = 50,
        num_points: int = 100
    ) -> Dict:
        """
        Analiza el sistema a lo largo de todo el recorrido.

        Calcula leverage ratios, desplazamientos del shock, y métricas
        de progresividad para un rango completo de desplazamiento de rueda.

        Args:
            travel_min: Desplazamiento mínimo de rueda en mm (negativo = extensión)
            travel_max: Desplazamiento máximo de rueda en mm (positivo = compresión)
            num_points: Número de puntos a calcular

        Returns:
            Diccionario con resultados del análisis:
                - wheel_travel: Array de desplazamientos de rueda (mm)
                - shock_travel: Array de desplazamientos de shock (mm)
                - shock_velocity: Array de velocidades de shock relativas
                - leverage_ratio: Array de ratios instantáneos
                - progression_percent: Porcentaje de progresividad
                - lr_initial: Leverage ratio en posición neutral
                - lr_max: Leverage ratio máximo
                - lr_min: Leverage ratio mínimo
                - lr_average: Leverage ratio promedio
                - system_type: Tipo de sistema (progresivo/lineal/regresivo)
        """
        # Generar puntos de análisis
        wheel_travel = np.linspace(travel_min, travel_max, num_points)
        shock_travel = np.zeros_like(wheel_travel)
        leverage_ratios = np.zeros_like(wheel_travel)
        shock_velocity = np.zeros_like(wheel_travel)

        # Calcular para cada posición
        for i, wt in enumerate(wheel_travel):
            try:
                shock_pos = self.suspension.calculate_shock_position(wt)
                shock_travel[i] = self._calculate_shock_travel(shock_pos)
                leverage_ratios[i] = self.suspension.calculate_leverage_ratio(wt)

                # Velocidad relativa del shock (1/LR)
                if leverage_ratios[i] > 0:
                    shock_velocity[i] = 1.0 / leverage_ratios[i]
                else:
                    shock_velocity[i] = np.nan

            except Exception as e:
                # Si hay error, marcar como NaN
                shock_travel[i] = np.nan
                leverage_ratios[i] = np.nan
                shock_velocity[i] = np.nan
                print(f"Advertencia: Error en posición {wt:.1f} mm: {e}")

        # Calcular métricas de progresividad
        progression_percent = self._calculate_progression(leverage_ratios, num_points)
        system_type = self._classify_system_type(progression_percent)

        # Estadísticas
        valid_ratios = leverage_ratios[~np.isnan(leverage_ratios)]
        mid_point = num_points // 2

        return {
            'wheel_travel': wheel_travel,
            'shock_travel': shock_travel,
            'shock_velocity': shock_velocity,
            'leverage_ratio': leverage_ratios,
            'progression_percent': progression_percent,
            'lr_initial': leverage_ratios[mid_point] if not np.isnan(leverage_ratios[mid_point]) else np.nan,
            'lr_max': np.nanmax(valid_ratios) if len(valid_ratios) > 0 else np.nan,
            'lr_min': np.nanmin(valid_ratios) if len(valid_ratios) > 0 else np.nan,
            'lr_average': np.nanmean(valid_ratios) if len(valid_ratios) > 0 else np.nan,
            'system_type': system_type,
        }

    def _calculate_shock_travel(self, shock_pos: Point) -> float:
        """
        Calcula el desplazamiento del shock respecto a su posición inicial.

        Args:
            shock_pos: Posición actual del anclaje del shock en el basculante

        Returns:
            Desplazamiento del shock en mm (positivo = compresión)
        """
        initial_length = self.suspension.initial_shock_length
        current_length = shock_pos.distance_to(
            self.suspension._get_shock_chassis_mount()
        )
        return current_length - initial_length

    def _calculate_progression(self, leverage_ratios: np.ndarray, num_points: int) -> float:
        """
        Calcula el porcentaje de progresividad del sistema.

        Compara el leverage ratio al final de la compresión con el ratio inicial.
        - Positivo: Progresivo (ratio aumenta en compresión)
        - Negativo: Regresivo (ratio disminuye en compresión)
        - ~0: Lineal (ratio constante)

        Args:
            leverage_ratios: Array de leverage ratios
            num_points: Número total de puntos

        Returns:
            Porcentaje de progresividad
        """
        mid_point = num_points // 2

        # Usar posición neutral y final de compresión
        if np.isnan(leverage_ratios[mid_point]) or np.isnan(leverage_ratios[-1]):
            return np.nan

        lr_initial = leverage_ratios[mid_point]
        lr_end_stroke = leverage_ratios[-1]

        if lr_initial == 0:
            return np.nan

        return ((lr_end_stroke - lr_initial) / lr_initial) * 100

    def _classify_system_type(self, progression_percent: float) -> str:
        """
        Clasifica el tipo de sistema según su progresividad.

        Args:
            progression_percent: Porcentaje de progresividad

        Returns:
            'progresivo', 'lineal', o 'regresivo'
        """
        if np.isnan(progression_percent):
            return 'desconocido'

        if progression_percent > 5:
            return 'progresivo'
        elif progression_percent < -5:
            return 'regresivo'
        else:
            return 'lineal'

    def calculate_wheel_rate(
        self,
        wheel_displacement: float,
        spring_rate: float
    ) -> float:
        """
        Calcula el wheel rate (rigidez efectiva en la rueda).

        El wheel rate es la rigidez percibida en la rueda dado el
        spring rate del muelle del amortiguador:

            wheel_rate = spring_rate / (leverage_ratio^2)

        Args:
            wheel_displacement: Posición de la rueda en mm
            spring_rate: Rigidez del muelle en N/mm

        Returns:
            Wheel rate en N/mm
        """
        lr = self.suspension.calculate_leverage_ratio(wheel_displacement)

        if lr <= 0 or np.isnan(lr) or np.isinf(lr):
            raise ValueError(f"Leverage ratio inválido: {lr}")

        return spring_rate / (lr ** 2)

    def find_optimal_spring_rate(
        self,
        target_wheel_rate: float,
        wheel_displacement: float = 0
    ) -> float:
        """
        Encuentra el spring rate necesario para lograr un wheel rate objetivo.

        Args:
            target_wheel_rate: Wheel rate deseado en N/mm
            wheel_displacement: Posición para el cálculo (default: neutral)

        Returns:
            Spring rate necesario en N/mm
        """
        lr = self.suspension.calculate_leverage_ratio(wheel_displacement)

        if lr <= 0 or np.isnan(lr) or np.isinf(lr):
            raise ValueError(f"Leverage ratio inválido: {lr}")

        return target_wheel_rate * (lr ** 2)

    def compare_positions(
        self,
        position1: float,
        position2: float
    ) -> Dict:
        """
        Compara las características cinemáticas en dos posiciones diferentes.

        Args:
            position1: Primera posición de rueda en mm
            position2: Segunda posición de rueda en mm

        Returns:
            Diccionario con comparación de métricas
        """
        lr1 = self.suspension.calculate_leverage_ratio(position1)
        lr2 = self.suspension.calculate_leverage_ratio(position2)

        shock_pos1 = self.suspension.calculate_shock_position(position1)
        shock_pos2 = self.suspension.calculate_shock_position(position2)

        shock_travel1 = self._calculate_shock_travel(shock_pos1)
        shock_travel2 = self._calculate_shock_travel(shock_pos2)

        return {
            'position1': {
                'wheel_displacement': position1,
                'shock_travel': shock_travel1,
                'leverage_ratio': lr1,
            },
            'position2': {
                'wheel_displacement': position2,
                'shock_travel': shock_travel2,
                'leverage_ratio': lr2,
            },
            'difference': {
                'wheel_displacement': position2 - position1,
                'shock_travel': shock_travel2 - shock_travel1,
                'leverage_ratio': lr2 - lr1,
                'lr_change_percent': ((lr2 - lr1) / lr1) * 100 if lr1 != 0 else np.nan,
            }
        }

    def get_summary(self) -> str:
        """
        Genera un resumen textual del análisis del sistema.

        Returns:
            String con resumen del análisis
        """
        # Analizar rango típico
        results = self.analyze_travel_range()

        summary = []
        summary.append("=" * 60)
        summary.append("RESUMEN DE ANÁLISIS CINEMÁTICO")
        summary.append("=" * 60)
        summary.append(f"Sistema: {self.suspension.__class__.__name__}")
        summary.append(f"\nLeverage Ratio:")
        summary.append(f"  Inicial (neutral):  {results['lr_initial']:.3f}")
        summary.append(f"  Promedio:           {results['lr_average']:.3f}")
        summary.append(f"  Mínimo:             {results['lr_min']:.3f}")
        summary.append(f"  Máximo:             {results['lr_max']:.3f}")
        summary.append(f"\nProgresividad:        {results['progression_percent']:.2f}%")
        summary.append(f"Tipo de sistema:      {results['system_type'].upper()}")

        if results['system_type'] == 'progresivo':
            summary.append("  -> El ratio aumenta en compresión (más suave al final)")
        elif results['system_type'] == 'regresivo':
            summary.append("  -> El ratio disminuye en compresión (más rígido al final)")
        else:
            summary.append("  -> El ratio se mantiene aproximadamente constante")

        summary.append("=" * 60)

        return '\n'.join(summary)
