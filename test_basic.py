"""
Script de prueba básica del sistema.
"""

print("=" * 70)
print("PRUEBA BASICA DEL SISTEMA DE ANALISIS DE CINEMATICA")
print("=" * 70)

# Test 1: Importaciones
print("\n1. Probando importaciones...")
try:
    from src.core.geometry import Point, Vector2D, Link
    from src.suspension.direct_shock import DirectShockSuspension, DirectShockGeometry
    from src.analysis.leverage_ratio import LeverageAnalyzer
    from src.visualization.plotter import SuspensionPlotter
    from src.visualization.animator import SuspensionAnimator
    from examples.sample_configs import get_typical_sportbike_geometry
    print("   ✓ Todas las importaciones exitosas")
except Exception as e:
    print(f"   ✗ Error en importaciones: {e}")
    exit(1)

# Test 2: Crear geometría
print("\n2. Creando geometría de ejemplo (sportbike)...")
try:
    geometry = get_typical_sportbike_geometry()
    print(f"   ✓ Geometría creada: basculante de {geometry.swingarm_length} mm")
except Exception as e:
    print(f"   ✗ Error creando geometría: {e}")
    exit(1)

# Test 3: Crear sistema de suspensión
print("\n3. Creando sistema de suspensión...")
try:
    suspension = DirectShockSuspension(geometry)
    print(f"   ✓ Sistema creado, longitud inicial shock: {suspension.initial_shock_length:.2f} mm")
except Exception as e:
    print(f"   ✗ Error creando suspensión: {e}")
    exit(1)

# Test 4: Validar geometría
print("\n4. Validando geometría...")
try:
    suspension.validate_geometry()
    print("   ✓ Geometría válida")
except Exception as e:
    print(f"   ✗ Error validando geometría: {e}")
    exit(1)

# Test 5: Calcular leverage ratio
print("\n5. Calculando leverage ratio en posición neutral...")
try:
    lr = suspension.calculate_leverage_ratio(0)
    print(f"   ✓ Leverage ratio en neutral: {lr:.3f}")
except Exception as e:
    print(f"   ✗ Error calculando LR: {e}")
    exit(1)

# Test 6: Calcular posición del shock
print("\n6. Calculando posición del shock...")
try:
    shock_pos = suspension.calculate_shock_position(0)
    print(f"   ✓ Posición shock: ({shock_pos.x:.1f}, {shock_pos.y:.1f}) mm")
except Exception as e:
    print(f"   ✗ Error calculando posición: {e}")
    exit(1)

# Test 7: Obtener todos los puntos
print("\n7. Obteniendo puntos clave...")
try:
    points = suspension.get_all_points(0)
    print(f"   ✓ {len(points)} puntos obtenidos: {list(points.keys())}")
except Exception as e:
    print(f"   ✗ Error obteniendo puntos: {e}")
    exit(1)

# Test 8: Análisis de leverage ratio
print("\n8. Ejecutando análisis completo...")
try:
    analyzer = LeverageAnalyzer(suspension)
    results = analyzer.analyze_travel_range(-30, 30, num_points=50)
    print(f"   ✓ Análisis completado:")
    print(f"      - LR inicial: {results['lr_initial']:.3f}")
    print(f"      - LR promedio: {results['lr_average']:.3f}")
    print(f"      - Progresividad: {results['progression_percent']:.2f}%")
    print(f"      - Tipo: {results['system_type']}")
except Exception as e:
    print(f"   ✗ Error en análisis: {e}")
    exit(1)

# Test 9: Test de diferentes configuraciones
print("\n9. Probando diferentes configuraciones predefinidas...")
try:
    from examples.sample_configs import PRESET_GEOMETRIES
    configs_tested = 0
    for name, get_geo_func in PRESET_GEOMETRIES.items():
        geo = get_geo_func()
        susp = DirectShockSuspension(geo)
        lr = susp.calculate_leverage_ratio(0)
        configs_tested += 1
        print(f"   ✓ {name}: LR inicial = {lr:.3f}")
    print(f"   {configs_tested} configuraciones probadas exitosamente")
except Exception as e:
    print(f"   ✗ Error probando configuraciones: {e}")
    exit(1)

# Test 10: Test de clases de geometría
print("\n10. Probando clases de geometría...")
try:
    p1 = Point(0, 0)
    p2 = Point(100, 100)
    dist = p1.distance_to(p2)
    print(f"   ✓ Distancia entre puntos: {dist:.2f} mm")

    p3 = p2.rotate_around(p1, 3.14159 / 2)  # 90 grados
    print(f"   ✓ Rotación: nuevo punto en ({p3.x:.1f}, {p3.y:.1f})")

    vec = Vector2D.from_points(p1, p2)
    mag = vec.magnitude()
    print(f"   ✓ Vector magnitud: {mag:.2f}")
except Exception as e:
    print(f"   ✗ Error en geometría: {e}")
    exit(1)

# Resumen final
print("\n" + "=" * 70)
print("RESULTADO: ✓ TODOS LOS TESTS PASARON EXITOSAMENTE")
print("=" * 70)
print("\nEl sistema está listo para usar. Ejecuta 'python main.py' para iniciar.")
print("=" * 70)
