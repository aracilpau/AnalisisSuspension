"""
Clases fundamentales para geometría 2D.

Este módulo proporciona las clases básicas para representar y manipular
geometría 2D necesaria para el análisis de cinemática de suspensiones.
"""

import numpy as np
from typing import Tuple


class Point:
    """
    Representa un punto 2D en el espacio.

    Attributes:
        x (float): Coordenada X en milímetros
        y (float): Coordenada Y en milímetros
    """

    def __init__(self, x: float, y: float):
        """
        Inicializa un punto 2D.

        Args:
            x: Coordenada X en milímetros
            y: Coordenada Y en milímetros
        """
        self.x = float(x)
        self.y = float(y)

    def distance_to(self, other: 'Point') -> float:
        """
        Calcula la distancia euclidiana a otro punto.

        Args:
            other: Otro punto

        Returns:
            Distancia en milímetros
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return np.sqrt(dx**2 + dy**2)

    def rotate_around(self, pivot: 'Point', angle: float) -> 'Point':
        """
        Rota este punto alrededor de un pivote dado un ángulo.

        Args:
            pivot: Punto alrededor del cual rotar
            angle: Ángulo de rotación en radianes (positivo = antihorario)

        Returns:
            Nuevo punto rotado
        """
        # Trasladar al origen
        dx = self.x - pivot.x
        dy = self.y - pivot.y

        # Aplicar rotación
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)

        x_rot = dx * cos_a - dy * sin_a
        y_rot = dx * sin_a + dy * cos_a

        # Trasladar de vuelta
        return Point(x_rot + pivot.x, y_rot + pivot.y)

    def to_array(self) -> np.ndarray:
        """
        Convierte el punto a numpy array.

        Returns:
            Array numpy [x, y]
        """
        return np.array([self.x, self.y])

    def __repr__(self) -> str:
        return f"Point({self.x:.2f}, {self.y:.2f})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return False
        return np.isclose(self.x, other.x) and np.isclose(self.y, other.y)


class Vector2D:
    """
    Vector 2D con operaciones vectoriales.

    Attributes:
        x (float): Componente X
        y (float): Componente Y
    """

    def __init__(self, x: float, y: float):
        """
        Inicializa un vector 2D.

        Args:
            x: Componente X
            y: Componente Y
        """
        self.x = float(x)
        self.y = float(y)

    @classmethod
    def from_points(cls, start: Point, end: Point) -> 'Vector2D':
        """
        Crea un vector desde un punto inicial a un punto final.

        Args:
            start: Punto inicial
            end: Punto final

        Returns:
            Vector2D desde start hasta end
        """
        return cls(end.x - start.x, end.y - start.y)

    def magnitude(self) -> float:
        """
        Calcula la magnitud (longitud) del vector.

        Returns:
            Magnitud del vector
        """
        return np.sqrt(self.x**2 + self.y**2)

    def normalize(self) -> 'Vector2D':
        """
        Retorna un vector unitario en la misma dirección.

        Returns:
            Vector normalizado (magnitud = 1)

        Raises:
            ValueError: Si el vector tiene magnitud cero
        """
        mag = self.magnitude()
        if mag < 1e-10:
            raise ValueError("No se puede normalizar un vector de magnitud cero")
        return Vector2D(self.x / mag, self.y / mag)

    def dot(self, other: 'Vector2D') -> float:
        """
        Calcula el producto escalar con otro vector.

        Args:
            other: Otro vector

        Returns:
            Producto escalar
        """
        return self.x * other.x + self.y * other.y

    def angle_between(self, other: 'Vector2D') -> float:
        """
        Calcula el ángulo entre este vector y otro.

        Args:
            other: Otro vector

        Returns:
            Ángulo en radianes (0 a π)
        """
        dot_product = self.dot(other)
        mag_product = self.magnitude() * other.magnitude()

        if mag_product < 1e-10:
            raise ValueError("No se puede calcular ángulo con vectores de magnitud cero")

        cos_angle = np.clip(dot_product / mag_product, -1.0, 1.0)
        return np.arccos(cos_angle)

    def angle(self) -> float:
        """
        Calcula el ángulo del vector respecto al eje X positivo.

        Returns:
            Ángulo en radianes (-π a π)
        """
        return np.arctan2(self.y, self.x)

    def to_array(self) -> np.ndarray:
        """
        Convierte el vector a numpy array.

        Returns:
            Array numpy [x, y]
        """
        return np.array([self.x, self.y])

    def __repr__(self) -> str:
        return f"Vector2D({self.x:.2f}, {self.y:.2f})"

    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        """Suma de vectores"""
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        """Resta de vectores"""
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Vector2D':
        """Multiplicación por escalar"""
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> 'Vector2D':
        """Multiplicación por escalar (orden inverso)"""
        return self.__mul__(scalar)


class Link:
    """
    Representa un enlace rígido entre dos puntos.

    Un enlace mantiene una distancia constante entre dos puntos,
    similar a una barra rígida o un brazo mecánico.

    Attributes:
        point_a (Point): Primer punto del enlace
        point_b (Point): Segundo punto del enlace
    """

    def __init__(self, point_a: Point, point_b: Point):
        """
        Inicializa un enlace entre dos puntos.

        Args:
            point_a: Primer punto
            point_b: Segundo punto
        """
        self.point_a = point_a
        self.point_b = point_b
        self._length = point_a.distance_to(point_b)

    @property
    def length(self) -> float:
        """
        Longitud del enlace (constante).

        Returns:
            Longitud en milímetros
        """
        return self._length

    @property
    def angle(self) -> float:
        """
        Ángulo actual del enlace respecto al eje X.

        Returns:
            Ángulo en radianes (-π a π)
        """
        vec = Vector2D.from_points(self.point_a, self.point_b)
        return vec.angle()

    def get_point_b_from_angle(self, pivot: Point, angle: float) -> Point:
        """
        Calcula la posición de point_b dado un ángulo de rotación.

        Asume que el enlace pivotea alrededor del punto 'pivot' (normalmente point_a)
        y calcula dónde estaría point_b si el enlace estuviera en el ángulo dado.

        Args:
            pivot: Punto alrededor del cual pivotea el enlace
            angle: Ángulo deseado en radianes

        Returns:
            Nueva posición de point_b
        """
        x = pivot.x + self.length * np.cos(angle)
        y = pivot.y + self.length * np.sin(angle)
        return Point(x, y)

    def update_points(self, point_a: Point, point_b: Point):
        """
        Actualiza las posiciones de los puntos del enlace.

        Args:
            point_a: Nueva posición del primer punto
            point_b: Nueva posición del segundo punto

        Raises:
            ValueError: Si la nueva distancia no coincide con la longitud del enlace
        """
        new_length = point_a.distance_to(point_b)
        if not np.isclose(new_length, self._length, rtol=1e-3):
            raise ValueError(
                f"La nueva distancia ({new_length:.2f} mm) no coincide "
                f"con la longitud del enlace ({self._length:.2f} mm)"
            )
        self.point_a = point_a
        self.point_b = point_b

    def __repr__(self) -> str:
        return f"Link({self.point_a}, {self.point_b}, length={self.length:.2f})"
