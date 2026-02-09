"""
Programa principal interactivo para análisis de cinemática de suspensiones.

Este es el punto de entrada principal del programa. Proporciona un menú
interactivo para configurar, analizar y visualizar suspensiones de motocicletas.
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
import csv

from src.core.geometry import Point
from src.suspension.direct_shock import DirectShockSuspension, DirectShockGeometry
from src.analysis.leverage_ratio import LeverageAnalyzer
from src.visualization.plotter import SuspensionPlotter
from src.visualization.animator import SuspensionAnimator
from examples.sample_configs import PRESET_GEOMETRIES, list_available_presets


def print_header():
    """Imprime el encabezado del programa."""
    print("\n" + "=" * 70)
    print(" " * 15 + "ANALIZADOR DE CINEMÁTICA DE SUSPENSIONES")
    print(" " * 20 + "Equipo MotorStudent")
    print("=" * 70)


def print_menu():
    """Imprime el menú principal."""
    print("\n" + "=" * 70)
    print(" " * 25 + "MENU PRINCIPAL")
    print("=" * 70)
    print("  1. Visualizar geometría en posición específica")
    print("  2. Analizar curva de leverage ratio")
    print("  3. Animar movimiento de suspensión")
    print("  4. Calcular leverage ratio en posición específica")
    print("  5. Exportar datos de análisis a CSV")
    print("  6. Modificar geometría")
    print("  7. Mostrar resumen de configuración actual")
    print("  0. Salir")
    print("=" * 70)


def get_user_geometry() -> DirectShockGeometry:
    """
    Obtiene la geometría del usuario (interactivo o predefinido).

    Returns:
        DirectShockGeometry configurado
    """
    print("\n" + "=" * 70)
    print(" " * 20 + "CONFIGURACION DE GEOMETRIA")
    print("=" * 70)

    list_available_presets()

    print("\nOpciones:")
    print("  1-5. Usar una configuración predefinida")
    print("  6. Introducir geometría personalizada")

    while True:
        choice = input("\nSelecciona opción [1-6]: ").strip()

        if choice == '1':
            return PRESET_GEOMETRIES['sportbike']()
        elif choice == '2':
            return PRESET_GEOMETRIES['enduro']()
        elif choice == '3':
            return PRESET_GEOMETRIES['supermoto']()
        elif choice == '4':
            return PRESET_GEOMETRIES['touring']()
        elif choice == '5':
            return PRESET_GEOMETRIES['motogp']()
        elif choice == '6':
            return input_custom_geometry()
        else:
            print("Opción no válida. Intenta de nuevo.")


def input_custom_geometry() -> DirectShockGeometry:
    """
    Input interactivo de geometría personalizada.

    Returns:
        DirectShockGeometry personalizado
    """
    print("\n" + "-" * 70)
    print(" " * 15 + "INTRODUCCION DE GEOMETRIA PERSONALIZADA")
    print("-" * 70)
    print("\nTodas las distancias en milímetros (mm), ángulos en grados.")
    print("Presiona Enter para usar el valor por defecto entre corchetes.\n")

    # Basculante
    print("--- BASCULANTE ---")
    swingarm_length = float(input("Longitud del basculante [600]: ").strip() or 600)
    swingarm_angle = float(input("Ángulo inicial (grados) [12]: ").strip() or 12)

    # Anclajes shock
    print("\n--- ANCLAJE SHOCK EN BASCULANTE (coordenadas locales) ---")
    print("Estas coordenadas son relativas al basculante en posición horizontal.")
    shock_sw_x = float(input("Posición X (mm) [200]: ").strip() or 200)
    shock_sw_y = float(input("Posición Y (mm) [60]: ").strip() or 60)

    print("\n--- ANCLAJE SHOCK EN CHASIS (coordenadas globales) ---")
    print("Estas coordenadas son fijas en el espacio global.")
    shock_ch_x = float(input("Posición X (mm) [120]: ").strip() or 120)
    shock_ch_y = float(input("Posición Y (mm) [250]: ").strip() or 250)

    # Rueda
    wheel_radius = float(input("\nRadio de rueda (mm) [310]: ").strip() or 310)

    geometry = DirectShockGeometry(
        swingarm_pivot=Point(0, 0),
        swingarm_length=swingarm_length,
        swingarm_initial_angle=swingarm_angle,
        shock_swingarm_offset=Point(shock_sw_x, shock_sw_y),
        shock_chassis_mount=Point(shock_ch_x, shock_ch_y),
        wheel_radius=wheel_radius
    )

    print("\nGeometría personalizada creada exitosamente.")
    return geometry


def visualize_geometry(suspension: DirectShockSuspension):
    """
    Visualiza la geometría en una posición específica.

    Args:
        suspension: Sistema de suspensión
    """
    print("\n" + "-" * 70)
    print("VISUALIZACION DE GEOMETRIA")
    print("-" * 70)

    wheel_disp_str = input("Desplazamiento de rueda en mm [0]: ").strip()
    wheel_disp = float(wheel_disp_str) if wheel_disp_str else 0.0

    print(f"\nGenerando visualización para desplazamiento de {wheel_disp:.1f} mm...")

    plotter = SuspensionPlotter(suspension)
    fig, ax = plotter.plot_geometry(wheel_disp)
    plt.show()

    print("Visualización completada.")


def analyze_leverage_curve(suspension: DirectShockSuspension):
    """
    Analiza y muestra la curva de leverage ratio.

    Args:
        suspension: Sistema de suspensión
    """
    print("\n" + "-" * 70)
    print("ANALISIS DE CURVA DE LEVERAGE RATIO")
    print("-" * 70)

    travel_min_str = input("Desplazamiento mínimo en mm [-50]: ").strip()
    travel_min = float(travel_min_str) if travel_min_str else -50.0

    travel_max_str = input("Desplazamiento máximo en mm [50]: ").strip()
    travel_max = float(travel_max_str) if travel_max_str else 50.0

    print(f"\nCalculando análisis cinemático...")
    print(f"Rango: {travel_min:.1f} mm a {travel_max:.1f} mm")

    analyzer = LeverageAnalyzer(suspension)
    results = analyzer.analyze_travel_range(travel_min, travel_max, num_points=100)

    # Mostrar resultados en consola
    print("\n" + "=" * 70)
    print(" " * 22 + "RESULTADOS DEL ANALISIS")
    print("=" * 70)
    print(f"Leverage Ratio inicial (neutral):  {results['lr_initial']:.3f}")
    print(f"Leverage Ratio promedio:           {results['lr_average']:.3f}")
    print(f"Leverage Ratio máximo:             {results['lr_max']:.3f}")
    print(f"Leverage Ratio mínimo:             {results['lr_min']:.3f}")
    print(f"\nProgresividad:                     {results['progression_percent']:.2f}%")
    print(f"Tipo de sistema:                   {results['system_type'].upper()}")

    if results['system_type'] == 'progresivo':
        print("\n  -> Sistema PROGRESIVO: El ratio aumenta en compresión.")
        print("     Suspensión más suave al inicio, más rígida al final del recorrido.")
    elif results['system_type'] == 'regresivo':
        print("\n  -> Sistema REGRESIVO: El ratio disminuye en compresión.")
        print("     Suspensión más rígida al inicio, más suave al final del recorrido.")
    else:
        print("\n  -> Sistema LINEAL: El ratio se mantiene aproximadamente constante.")
        print("     Comportamiento consistente a lo largo del recorrido.")

    print("=" * 70)

    # Visualizar gráficos
    print("\nGenerando gráficos...")
    plotter = SuspensionPlotter(suspension)
    fig, axes = plotter.plot_leverage_curve(results)
    plt.show()

    print("Análisis completado.")


def animate_suspension(suspension: DirectShockSuspension):
    """
    Crea y muestra animación del movimiento.

    Args:
        suspension: Sistema de suspensión
    """
    print("\n" + "-" * 70)
    print("ANIMACION DE MOVIMIENTO")
    print("-" * 70)

    travel_min_str = input("Desplazamiento mínimo en mm [-50]: ").strip()
    travel_min = float(travel_min_str) if travel_min_str else -50.0

    travel_max_str = input("Desplazamiento máximo en mm [50]: ").strip()
    travel_max = float(travel_max_str) if travel_max_str else 50.0

    show_trail = input("¿Mostrar rastro del movimiento? (s/n) [n]: ").strip().lower() == 's'

    print(f"\nGenerando animación...")
    print(f"Rango: {travel_min:.1f} mm a {travel_max:.1f} mm")
    print("Cierra la ventana de la animación para continuar.")

    plotter = SuspensionPlotter(suspension)
    animator = SuspensionAnimator(suspension, plotter)

    anim = animator.animate_travel(
        travel_range=(travel_min, travel_max),
        num_frames=100,
        interval=50,
        show_trail=show_trail
    )

    plt.show()

    print("Animación completada.")


def calculate_lr_at_position(suspension: DirectShockSuspension):
    """
    Calcula leverage ratio en una posición específica.

    Args:
        suspension: Sistema de suspensión
    """
    print("\n" + "-" * 70)
    print("CALCULO DE LEVERAGE RATIO EN POSICION ESPECIFICA")
    print("-" * 70)

    wheel_disp_str = input("Desplazamiento de rueda en mm [0]: ").strip()
    wheel_disp = float(wheel_disp_str) if wheel_disp_str else 0.0

    print(f"\nCalculando...")

    try:
        lr = suspension.calculate_leverage_ratio(wheel_disp)
        shock_pos = suspension.calculate_shock_position(wheel_disp)
        shock_length = shock_pos.distance_to(suspension.geometry.shock_chassis_mount)
        shock_travel = shock_length - suspension.initial_shock_length

        print("\n" + "=" * 70)
        print(" " * 27 + "RESULTADOS")
        print("=" * 70)
        print(f"Desplazamiento rueda:          {wheel_disp:+.2f} mm")
        print(f"Desplazamiento shock:          {shock_travel:+.2f} mm")
        print(f"Leverage Ratio:                {lr:.3f}")
        print(f"Longitud actual del shock:     {shock_length:.2f} mm")
        print(f"Longitud inicial del shock:    {suspension.initial_shock_length:.2f} mm")
        print("=" * 70)

    except Exception as e:
        print(f"\nError en el cálculo: {e}")


def export_analysis_data(suspension: DirectShockSuspension):
    """
    Exporta datos de análisis a CSV.

    Args:
        suspension: Sistema de suspensión
    """
    print("\n" + "-" * 70)
    print("EXPORTAR DATOS A CSV")
    print("-" * 70)

    filename = input("Nombre de archivo (sin extensión) [analysis]: ").strip() or "analysis"

    travel_min_str = input("Desplazamiento mínimo en mm [-50]: ").strip()
    travel_min = float(travel_min_str) if travel_min_str else -50.0

    travel_max_str = input("Desplazamiento máximo en mm [50]: ").strip()
    travel_max = float(travel_max_str) if travel_max_str else 50.0

    num_points_str = input("Número de puntos [200]: ").strip()
    num_points = int(num_points_str) if num_points_str else 200

    print(f"\nCalculando datos...")

    analyzer = LeverageAnalyzer(suspension)
    results = analyzer.analyze_travel_range(travel_min, travel_max, num_points=num_points)

    output_file = f"{filename}.csv"

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Encabezado
            writer.writerow([
                'Wheel_Travel_mm',
                'Shock_Travel_mm',
                'Leverage_Ratio',
                'Shock_Velocity_Relative'
            ])

            # Datos
            for wt, st, lr, sv in zip(
                results['wheel_travel'],
                results['shock_travel'],
                results['leverage_ratio'],
                results['shock_velocity']
            ):
                writer.writerow([
                    f"{wt:.3f}",
                    f"{st:.3f}",
                    f"{lr:.4f}",
                    f"{sv:.4f}"
                ])

        print(f"\nDatos exportados exitosamente a: {output_file}")
        print(f"Total de puntos: {num_points}")

    except Exception as e:
        print(f"\nError exportando datos: {e}")


def show_configuration_summary(suspension: DirectShockSuspension):
    """
    Muestra un resumen de la configuración actual.

    Args:
        suspension: Sistema de suspensión
    """
    print("\n" + "=" * 70)
    print(" " * 18 + "RESUMEN DE CONFIGURACION ACTUAL")
    print("=" * 70)

    geo = suspension.geometry

    print("\nBASCULANTE:")
    print(f"  Pivote:                    ({geo.swingarm_pivot.x:.1f}, {geo.swingarm_pivot.y:.1f}) mm")
    print(f"  Longitud:                  {geo.swingarm_length:.1f} mm")
    print(f"  Ángulo inicial:            {geo.swingarm_initial_angle:.1f}°")

    print("\nANCLAJES DEL AMORTIGUADOR:")
    print(f"  Basculante (local):        ({geo.shock_swingarm_offset.x:.1f}, {geo.shock_swingarm_offset.y:.1f}) mm")
    print(f"  Chasis (global):           ({geo.shock_chassis_mount.x:.1f}, {geo.shock_chassis_mount.y:.1f}) mm")
    print(f"  Longitud inicial:          {suspension.initial_shock_length:.1f} mm")

    print("\nRUEDA:")
    print(f"  Radio:                     {geo.wheel_radius:.1f} mm")

    # Análisis rápido
    print("\nANALISIS RAPIDO:")
    analyzer = LeverageAnalyzer(suspension)
    results = analyzer.analyze_travel_range(-30, 30, num_points=50)

    print(f"  Leverage Ratio (neutral):  {results['lr_initial']:.3f}")
    print(f"  Progresividad:             {results['progression_percent']:.2f}%")
    print(f"  Tipo:                      {results['system_type'].upper()}")

    print("=" * 70)


def main():
    """Función principal del programa."""
    print_header()

    print("\nBienvenido al Analizador de Cinemática de Suspensiones.")
    print("Este programa te ayudará a analizar y optimizar la suspensión de tu motocicleta.\n")

    # Configuración inicial
    print("Primero, configura la geometría de la suspensión:")
    geometry = get_user_geometry()

    # Crear sistema de suspensión
    print("\nCreando sistema de suspensión...")
    try:
        suspension = DirectShockSuspension(geometry)
        suspension.validate_geometry()
        print("Sistema de suspensión creado y validado exitosamente.")
    except Exception as e:
        print(f"Error creando sistema de suspensión: {e}")
        sys.exit(1)

    # Bucle principal del menú
    while True:
        print_menu()

        choice = input("Selecciona opción [0-7]: ").strip()

        try:
            if choice == "1":
                visualize_geometry(suspension)
            elif choice == "2":
                analyze_leverage_curve(suspension)
            elif choice == "3":
                animate_suspension(suspension)
            elif choice == "4":
                calculate_lr_at_position(suspension)
            elif choice == "5":
                export_analysis_data(suspension)
            elif choice == "6":
                print("\nModificando geometría...")
                geometry = get_user_geometry()
                suspension = DirectShockSuspension(geometry)
                suspension.validate_geometry()
                print("Geometría actualizada exitosamente.")
            elif choice == "7":
                show_configuration_summary(suspension)
            elif choice == "0":
                print("\n" + "=" * 70)
                print("Gracias por usar el Analizador de Cinemática de Suspensiones.")
                print("Equipo MotorStudent")
                print("=" * 70 + "\n")
                break
            else:
                print("\nOpción no válida. Por favor, selecciona una opción del 0 al 7.")

        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario.")
        except Exception as e:
            print(f"\nError: {e}")
            print("Por favor, intenta de nuevo.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma terminado por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError fatal: {e}")
        sys.exit(1)
