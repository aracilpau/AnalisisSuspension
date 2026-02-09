"""
Configuraciones predefinidas de ejemplo para diferentes tipos de motocicletas.

Este módulo proporciona geometrías de suspensión típicas para varios
tipos de motocicletas, útiles como punto de partida para análisis.
"""

from src.core.geometry import Point
from src.suspension.direct_shock import DirectShockGeometry


def get_typical_sportbike_geometry() -> DirectShockGeometry:
    """
    Geometría típica de motocicleta deportiva (sportbike).

    Características:
        - Basculante relativamente corto (600 mm)
        - Leverage ratio medio (~2.5-3.0)
        - Ligeramente progresivo para mejor control
        - Ángulo moderado del basculante

    Returns:
        DirectShockGeometry configurado para sportbike
    """
    return DirectShockGeometry(
        swingarm_pivot=Point(0, 0),
        swingarm_length=600,  # 600mm basculante
        swingarm_initial_angle=12,  # 12° hacia arriba
        shock_swingarm_offset=Point(200, 60),  # Anclaje en basculante (coordenadas locales)
        shock_chassis_mount=Point(120, 250),    # Anclaje en chasis (coordenadas globales)
        wheel_radius=310  # Rueda de 17" (~310mm radio)
    )


def get_enduro_geometry() -> DirectShockGeometry:
    """
    Geometría típica de motocicleta de enduro.

    Características:
        - Basculante de longitud media (580 mm)
        - Leverage ratio más alto (~3.0-3.5) para mayor sensibilidad
        - Más progresivo para absorber impactos grandes
        - Ángulo mayor del basculante

    Returns:
        DirectShockGeometry configurado para enduro
    """
    return DirectShockGeometry(
        swingarm_pivot=Point(0, 0),
        swingarm_length=580,
        swingarm_initial_angle=15,  # 15° hacia arriba
        shock_swingarm_offset=Point(180, 80),
        shock_chassis_mount=Point(100, 300),
        wheel_radius=330  # Rueda de 18" o 19" (~330mm radio)
    )


def get_supermoto_geometry() -> DirectShockGeometry:
    """
    Geometría típica de motocicleta supermoto.

    Características:
        - Basculante más corto (560 mm)
        - Leverage ratio bajo (~2.3-2.7) para suspensión más rígida
        - Menos progresivo para mejor feedback en asfalto
        - Menor recorrido de suspensión

    Returns:
        DirectShockGeometry configurado para supermoto
    """
    return DirectShockGeometry(
        swingarm_pivot=Point(0, 0),
        swingarm_length=560,
        swingarm_initial_angle=10,  # 10° hacia arriba
        shock_swingarm_offset=Point(210, 50),
        shock_chassis_mount=Point(130, 220),
        wheel_radius=320  # Rueda de 17" (~320mm radio)
    )


def get_touring_geometry() -> DirectShockGeometry:
    """
    Geometría típica de motocicleta de turismo.

    Características:
        - Basculante largo (620 mm) para estabilidad
        - Leverage ratio medio-alto (~2.8-3.2) para confort
        - Progresivo para carga variable
        - Diseño orientado a confort

    Returns:
        DirectShockGeometry configurado para touring
    """
    return DirectShockGeometry(
        swingarm_pivot=Point(0, 0),
        swingarm_length=620,
        swingarm_initial_angle=11,  # 11° hacia arriba
        shock_swingarm_offset=Point(190, 70),
        shock_chassis_mount=Point(110, 260),
        wheel_radius=315  # Rueda de 17" (~315mm radio)
    )


def get_motogp_inspired_geometry() -> DirectShockGeometry:
    """
    Geometría inspirada en MotoGP (valores aproximados).

    Características:
        - Basculante largo (630+ mm) para máxima tracción
        - Leverage ratio optimizado (~2.6-2.9)
        - Ligeramente progresivo
        - Geometría agresiva de competición

    Returns:
        DirectShockGeometry configurado estilo MotoGP
    """
    return DirectShockGeometry(
        swingarm_pivot=Point(0, 0),
        swingarm_length=635,
        swingarm_initial_angle=13,  # 13° hacia arriba
        shock_swingarm_offset=Point(210, 65),
        shock_chassis_mount=Point(125, 245),
        wheel_radius=305  # Rueda de 16.5" (~305mm radio) tipo slick de competición
    )


# Diccionario para acceso fácil a todas las configuraciones
PRESET_GEOMETRIES = {
    'sportbike': get_typical_sportbike_geometry,
    'enduro': get_enduro_geometry,
    'supermoto': get_supermoto_geometry,
    'touring': get_touring_geometry,
    'motogp': get_motogp_inspired_geometry,
}


def list_available_presets():
    """
    Lista todas las configuraciones predefinidas disponibles.
    """
    print("\nConfiguraciones predefinidas disponibles:")
    print("-" * 60)
    for name in PRESET_GEOMETRIES.keys():
        print(f"  - {name}")
    print("-" * 60)


def get_preset_geometry(preset_name: str) -> DirectShockGeometry:
    """
    Obtiene una geometría predefinida por nombre.

    Args:
        preset_name: Nombre de la configuración predefinida

    Returns:
        DirectShockGeometry correspondiente

    Raises:
        ValueError: Si el nombre no corresponde a ninguna configuración
    """
    if preset_name.lower() not in PRESET_GEOMETRIES:
        available = ', '.join(PRESET_GEOMETRIES.keys())
        raise ValueError(
            f"Configuración '{preset_name}' no encontrada. "
            f"Disponibles: {available}"
        )

    return PRESET_GEOMETRIES[preset_name.lower()]()
