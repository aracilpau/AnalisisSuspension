"""
Interfaz web para el Analizador de Cinemática de Suspensiones.
Flask backend que expone la funcionalidad del CLI como API REST.
"""
import sys
import os
import io
import base64
import json
import csv

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify, send_file
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

from src.core.geometry import Point
from src.suspension.direct_shock import DirectShockSuspension, DirectShockGeometry
from src.analysis.leverage_ratio import LeverageAnalyzer
from src.visualization.plotter import SuspensionPlotter
from src.visualization.animator import SuspensionAnimator
from examples.sample_configs import PRESET_GEOMETRIES

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')

# Store current suspension in memory
current_state = {
    'suspension': None,
    'geometry_name': None
}


def fig_to_base64(fig):
    """Convierte una figura matplotlib a base64 para mostrar en HTML."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


def create_geometry(params):
    """Crea geometría desde parámetros del formulario."""
    return DirectShockGeometry(
        swingarm_pivot=Point(0, 0),
        swingarm_length=float(params.get('swingarm_length', 600)),
        swingarm_initial_angle=float(params.get('swingarm_angle', 12)),
        shock_swingarm_offset=Point(
            float(params.get('shock_sw_x', 200)),
            float(params.get('shock_sw_y', 60))
        ),
        shock_chassis_mount=Point(
            float(params.get('shock_ch_x', 120)),
            float(params.get('shock_ch_y', 250))
        ),
        wheel_radius=float(params.get('wheel_radius', 310))
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/presets')
def get_presets():
    """Devuelve lista de presets disponibles."""
    presets = {
        'sportbike': {'name': 'Sportbike', 'desc': 'Deportiva de circuito'},
        'enduro': {'name': 'Enduro', 'desc': 'Todo terreno'},
        'supermoto': {'name': 'Supermoto', 'desc': 'Supermotard'},
        'touring': {'name': 'Touring', 'desc': 'Gran turismo'},
        'motogp': {'name': 'MotoGP', 'desc': 'Competición GP'}
    }
    return jsonify(presets)


@app.route('/api/preset/<name>')
def get_preset_values(name):
    """Devuelve los valores de un preset específico."""
    if name not in PRESET_GEOMETRIES:
        return jsonify({'error': 'Preset no encontrado'}), 404

    geo = PRESET_GEOMETRIES[name]()
    return jsonify({
        'swingarm_length': geo.swingarm_length,
        'swingarm_angle': geo.swingarm_initial_angle,
        'shock_sw_x': geo.shock_swingarm_offset.x,
        'shock_sw_y': geo.shock_swingarm_offset.y,
        'shock_ch_x': geo.shock_chassis_mount.x,
        'shock_ch_y': geo.shock_chassis_mount.y,
        'wheel_radius': geo.wheel_radius
    })


@app.route('/api/configure', methods=['POST'])
def configure():
    """Configura la geometría de la suspensión."""
    try:
        params = request.json
        geometry = create_geometry(params)
        suspension = DirectShockSuspension(geometry)
        suspension.validate_geometry()

        current_state['suspension'] = suspension
        current_state['geometry_name'] = params.get('preset_name', 'Personalizada')

        return jsonify({
            'success': True,
            'shock_length': round(suspension.initial_shock_length, 1),
            'message': 'Suspensión configurada correctamente'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/visualize', methods=['POST'])
def visualize():
    """Visualiza la geometría en una posición."""
    if not current_state['suspension']:
        return jsonify({'error': 'Configura la geometría primero'}), 400

    try:
        wheel_disp = float(request.json.get('wheel_displacement', 0))
        suspension = current_state['suspension']

        plotter = SuspensionPlotter(suspension)
        fig, ax = plotter.plot_geometry(wheel_disp)
        fig.set_facecolor('#1a1a2e')
        img = fig_to_base64(fig)

        return jsonify({'image': img})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analiza la curva de leverage ratio."""
    if not current_state['suspension']:
        return jsonify({'error': 'Configura la geometría primero'}), 400

    try:
        data = request.json
        travel_min = float(data.get('travel_min', -50))
        travel_max = float(data.get('travel_max', 50))

        suspension = current_state['suspension']
        analyzer = LeverageAnalyzer(suspension)
        results = analyzer.analyze_travel_range(travel_min, travel_max, num_points=100)

        # Generar gráficos
        plotter = SuspensionPlotter(suspension)
        fig, axes = plotter.plot_leverage_curve(results)
        fig.set_facecolor('#1a1a2e')
        img = fig_to_base64(fig)

        return jsonify({
            'image': img,
            'lr_initial': round(results['lr_initial'], 3),
            'lr_average': round(results['lr_average'], 3),
            'lr_max': round(results['lr_max'], 3),
            'lr_min': round(results['lr_min'], 3),
            'progression': round(results['progression_percent'], 2),
            'system_type': results['system_type']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/leverage', methods=['POST'])
def leverage_at_position():
    """Calcula leverage ratio en posición específica."""
    if not current_state['suspension']:
        return jsonify({'error': 'Configura la geometría primero'}), 400

    try:
        wheel_disp = float(request.json.get('wheel_displacement', 0))
        suspension = current_state['suspension']

        lr = suspension.calculate_leverage_ratio(wheel_disp)
        shock_pos = suspension.calculate_shock_position(wheel_disp)
        shock_length = shock_pos.distance_to(suspension.geometry.shock_chassis_mount)
        shock_travel = shock_length - suspension.initial_shock_length

        return jsonify({
            'wheel_displacement': round(wheel_disp, 2),
            'shock_travel': round(shock_travel, 2),
            'leverage_ratio': round(lr, 3),
            'shock_length': round(shock_length, 2),
            'initial_shock_length': round(suspension.initial_shock_length, 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/summary')
def summary():
    """Resumen de configuración actual."""
    if not current_state['suspension']:
        return jsonify({'error': 'Configura la geometría primero'}), 400

    suspension = current_state['suspension']
    geo = suspension.geometry

    analyzer = LeverageAnalyzer(suspension)
    results = analyzer.analyze_travel_range(-30, 30, num_points=50)

    return jsonify({
        'name': current_state['geometry_name'],
        'swingarm_pivot': {'x': geo.swingarm_pivot.x, 'y': geo.swingarm_pivot.y},
        'swingarm_length': geo.swingarm_length,
        'swingarm_angle': geo.swingarm_initial_angle,
        'shock_swingarm': {'x': geo.shock_swingarm_offset.x, 'y': geo.shock_swingarm_offset.y},
        'shock_chassis': {'x': geo.shock_chassis_mount.x, 'y': geo.shock_chassis_mount.y},
        'wheel_radius': geo.wheel_radius,
        'initial_shock_length': round(suspension.initial_shock_length, 1),
        'lr_neutral': round(results['lr_initial'], 3),
        'progression': round(results['progression_percent'], 2),
        'system_type': results['system_type']
    })


@app.route('/api/shock_to_wheel', methods=['POST'])
def shock_to_wheel():
    """Calcula el recorrido de rueda equivalente a un stroke de shock dado."""
    if not current_state['suspension']:
        return jsonify({'error': 'Configura la geometría primero'}), 400

    try:
        shock_stroke = float(request.json.get('shock_stroke', 59))
        suspension = current_state['suspension']

        # Search: find wheel displacement where shock compression = shock_stroke
        from scipy.optimize import brentq

        def shock_error(wheel_disp):
            shock_pos = suspension.calculate_shock_position(wheel_disp)
            shock_length = shock_pos.distance_to(suspension.geometry.shock_chassis_mount)
            shock_compression = suspension.initial_shock_length - shock_length
            return shock_compression - shock_stroke

        # Find wheel displacement where shock is fully compressed
        # Search in a wide range
        wheel_max = brentq(shock_error, 0, 300, xtol=0.01)

        # Also calculate average LR across the range
        analyzer = LeverageAnalyzer(suspension)
        results = analyzer.analyze_travel_range(0, wheel_max, num_points=50)

        return jsonify({
            'wheel_travel': round(wheel_max, 1),
            'shock_stroke': round(shock_stroke, 1),
            'lr_average': round(results['lr_average'], 3),
            'lr_initial': round(results['lr_initial'], 3),
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/sag', methods=['POST'])
def calculate_sag():
    """Calcula el sag estático de la suspensión."""
    try:
        data = request.json
        geometry = create_geometry(data)
        suspension = DirectShockSuspension(geometry)
        suspension.validate_geometry()

        spring_rate = float(data.get('spring_rate', 80))  # N/mm
        preload = float(data.get('preload', 10))  # mm
        weight = float(data.get('weight', 100))  # kg on rear wheel
        max_travel = float(data.get('max_travel', 120))  # mm

        weight_force = weight * 9.81  # N

        # Find equilibrium: spring_rate * (shock_compression + preload) = weight_force * LR
        # Search wheel displacement from 0 to max_travel
        from scipy.optimize import brentq

        def force_balance(wheel_disp):
            """Positive = spring wins, negative = weight wins."""
            if wheel_disp <= 0:
                return weight_force  # At 0 displacement, spring has preload but we start searching from 0
            try:
                shock_pos = suspension.calculate_shock_position(wheel_disp)
                shock_length = shock_pos.distance_to(suspension.geometry.shock_chassis_mount)
                shock_compression = suspension.initial_shock_length - shock_length
                if shock_compression < 0:
                    shock_compression = 0

                lr = abs(suspension.calculate_leverage_ratio(wheel_disp))
                spring_force = spring_rate * (shock_compression + preload)
                wheel_force_from_spring = spring_force / lr

                return wheel_force_from_spring - weight_force
            except Exception:
                return -weight_force

        # Check if sag exists in range
        f_at_0 = force_balance(0.01)
        f_at_max = force_balance(max_travel)

        if f_at_0 < 0:
            # Even with preload, weight wins at 0 — sag would be beyond range or preload too low
            # Still try to find it
            pass

        sag_wheel = 0
        try:
            if f_at_0 * f_at_max < 0:
                sag_wheel = brentq(force_balance, 0.01, max_travel, xtol=0.01)
            elif f_at_0 < 0:
                sag_wheel = max_travel  # Bottoms out
            else:
                sag_wheel = 0  # No sag (preload too high)
        except Exception:
            sag_wheel = 0

        # Calculate results at sag position
        shock_pos = suspension.calculate_shock_position(sag_wheel)
        shock_length = shock_pos.distance_to(suspension.geometry.shock_chassis_mount)
        shock_sag = suspension.initial_shock_length - shock_length
        lr_at_sag = abs(suspension.calculate_leverage_ratio(sag_wheel))
        spring_force = spring_rate * (max(shock_sag, 0) + preload)
        sag_percent = (sag_wheel / max_travel) * 100

        # Generate plot: LR curve with sag point marked
        analyzer = LeverageAnalyzer(suspension)
        results = analyzer.analyze_travel_range(0, max_travel, num_points=100)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        fig.set_facecolor('#1a1a2e')

        for ax in (ax1, ax2):
            ax.set_facecolor('#1a1a2e')
            ax.tick_params(colors='#aaa')
            ax.xaxis.label.set_color('#aaa')
            ax.yaxis.label.set_color('#aaa')
            ax.title.set_color('#eee')
            for spine in ax.spines.values():
                spine.set_color('#333')
            ax.grid(True, alpha=0.2, color='#555')

        # Plot 1: Force vs wheel displacement
        wheel_positions = np.linspace(0.1, max_travel, 100)
        spring_forces = []
        weight_forces = []
        for w in wheel_positions:
            try:
                sp = suspension.calculate_shock_position(w)
                sl = sp.distance_to(suspension.geometry.shock_chassis_mount)
                sc = max(suspension.initial_shock_length - sl, 0)
                lr_w = abs(suspension.calculate_leverage_ratio(w))
                sf = spring_rate * (sc + preload)
                wf = sf / lr_w
                spring_forces.append(wf)
                weight_forces.append(weight_force)
            except Exception:
                spring_forces.append(0)
                weight_forces.append(weight_force)

        ax1.plot(wheel_positions, spring_forces, color='#4ecca3', linewidth=2, label='Fuerza muelle (en rueda)')
        ax1.axhline(y=weight_force, color='#e94560', linewidth=2, linestyle='--', label=f'Peso ({weight_force:.0f} N)')
        if sag_wheel > 0:
            ax1.axvline(x=sag_wheel, color='#ffc947', linewidth=1.5, linestyle=':', alpha=0.8)
            ax1.plot(sag_wheel, weight_force, 'o', color='#ffc947', markersize=12, zorder=5, label=f'Sag = {sag_wheel:.1f} mm')
        ax1.set_xlabel('Desplazamiento rueda (mm)')
        ax1.set_ylabel('Fuerza (N)')
        ax1.set_title('Equilibrio de fuerzas')
        ax1.legend(facecolor='#252542', edgecolor='#333', labelcolor='#eee', fontsize=9)

        # Plot 2: LR curve with sag marked
        ax2.plot(results['wheel_travel'], results['leverage_ratio'], color='#4fc3f7', linewidth=2, label='Leverage Ratio')
        if sag_wheel > 0:
            ax2.axvline(x=sag_wheel, color='#ffc947', linewidth=1.5, linestyle=':', alpha=0.8)
            ax2.plot(sag_wheel, lr_at_sag, 'o', color='#ffc947', markersize=12, zorder=5, label=f'Sag (LR = {lr_at_sag:.3f})')
        ax2.set_xlabel('Desplazamiento rueda (mm)')
        ax2.set_ylabel('Leverage Ratio')
        ax2.set_title('LR con punto de Sag')
        ax2.legend(facecolor='#252542', edgecolor='#333', labelcolor='#eee', fontsize=9)

        plt.tight_layout()
        img = fig_to_base64(fig)

        return jsonify({
            'wheel_sag': round(sag_wheel, 1),
            'shock_sag': round(max(shock_sag, 0), 1),
            'sag_percent': round(sag_percent, 1),
            'lr_at_sag': round(lr_at_sag, 3),
            'spring_force': round(spring_force, 0),
            'wheel_force': round(weight_force, 0),
            'image': img
        })
    except Exception as e:
        plt.close('all')
        return jsonify({'error': str(e)}), 400


@app.route('/api/fork_sag', methods=['POST'])
def fork_sag():
    """Calcula el sag de la horquilla delantera (sistema directo, LR=1)."""
    try:
        data = request.json
        travel = float(data.get('travel', 110))        # mm
        spring_rate = float(data.get('spring_rate', 50))  # N/mm per spring
        preload = float(data.get('preload', 5))          # mm
        weight = float(data.get('weight', 95))            # kg on front wheel

        weight_force = weight * 9.81  # N
        # Two springs: total_rate = 2 * spring_rate
        total_rate = 2 * spring_rate

        # Equilibrium: total_rate * (sag + preload) = weight_force
        # sag = weight_force / total_rate - preload
        sag = weight_force / total_rate - preload

        if sag < 0:
            sag = 0  # Preload too high, no sag
        elif sag > travel:
            sag = travel  # Bottoms out

        sag_percent = (sag / travel) * 100
        spring_force = total_rate * (sag + preload)

        # Generate plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        fig.set_facecolor('#1a1a2e')

        for ax in (ax1, ax2):
            ax.set_facecolor('#1a1a2e')
            ax.tick_params(colors='#aaa')
            ax.xaxis.label.set_color('#aaa')
            ax.yaxis.label.set_color('#aaa')
            ax.title.set_color('#eee')
            for spine in ax.spines.values():
                spine.set_color('#333')
            ax.grid(True, alpha=0.2, color='#555')

        # Plot 1: Force vs displacement
        displacements = np.linspace(0, travel, 100)
        spring_forces = total_rate * (displacements + preload)

        ax1.plot(displacements, spring_forces, color='#4ecca3', linewidth=2, label='Fuerza muelles (2×)')
        ax1.axhline(y=weight_force, color='#e94560', linewidth=2, linestyle='--', label=f'Peso ({weight_force:.0f} N)')
        if 0 < sag < travel:
            ax1.axvline(x=sag, color='#ffc947', linewidth=1.5, linestyle=':', alpha=0.8)
            ax1.plot(sag, weight_force, 'o', color='#ffc947', markersize=12, zorder=5, label=f'Sag = {sag:.1f} mm')
        ax1.set_xlabel('Compresión horquilla (mm)')
        ax1.set_ylabel('Fuerza (N)')
        ax1.set_title('Equilibrio de fuerzas')
        ax1.legend(facecolor='#252542', edgecolor='#333', labelcolor='#eee', fontsize=9)

        # Plot 2: Sag bar chart for context
        ax2.barh(['Sag', 'Recorrido restante'], [sag, travel - sag],
                  color=['#ffc947', '#4ecca3'], height=0.5)
        ax2.set_xlim(0, travel)
        ax2.set_xlabel('mm')
        ax2.set_title(f'Uso del recorrido ({sag_percent:.1f}% sag)')
        # Add percentage text
        if sag > 0:
            ax2.text(sag / 2, 0, f'{sag:.1f} mm', ha='center', va='center', color='#1a1a2e', fontweight='bold')
        ax2.text((sag + travel) / 2, 1, f'{travel - sag:.1f} mm', ha='center', va='center', color='#1a1a2e', fontweight='bold')

        plt.tight_layout()
        img = fig_to_base64(fig)

        return jsonify({
            'sag': round(sag, 1),
            'sag_percent': round(sag_percent, 1),
            'spring_force': round(spring_force, 0),
            'weight_force': round(weight_force, 0),
            'total_rate': round(total_rate, 0),
            'travel': round(travel, 0),
            'image': img
        })
    except Exception as e:
        plt.close('all')
        return jsonify({'error': str(e)}), 400


@app.route('/api/fork_compare', methods=['POST'])
def fork_compare():
    """Compara sag para todos los muelles disponibles de la horquilla."""
    try:
        data = request.json
        travel = float(data.get('travel', 110))
        preload = float(data.get('preload', 5))
        weight = float(data.get('weight', 95))

        weight_force = weight * 9.81
        spring_rates = [35, 40, 45, 50, 55, 60, 65]
        results = []

        for k in spring_rates:
            total_rate = 2 * k
            sag = weight_force / total_rate - preload
            if sag < 0:
                sag = 0
            elif sag > travel:
                sag = travel
            sag_pct = (sag / travel) * 100
            results.append({
                'spring_rate': k,
                'sag': round(sag, 1),
                'sag_percent': round(sag_pct, 1),
                'total_rate': round(total_rate, 0)
            })

        # Generate comparison plot
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.set_facecolor('#1a1a2e')
        ax.set_facecolor('#1a1a2e')
        ax.tick_params(colors='#aaa')
        ax.xaxis.label.set_color('#aaa')
        ax.yaxis.label.set_color('#aaa')
        ax.title.set_color('#eee')
        for spine in ax.spines.values():
            spine.set_color('#333')
        ax.grid(True, alpha=0.2, color='#555', axis='y')

        sags = [r['sag'] for r in results]
        pcts = [r['sag_percent'] for r in results]
        labels = [f"{k} N/mm" for k in spring_rates]

        colors = []
        for p in pcts:
            if 25 <= p <= 33:
                colors.append('#4ecca3')  # green = optimal
            elif p < 25:
                colors.append('#4fc3f7')  # blue = stiff
            else:
                colors.append('#e94560')  # red = soft

        bars = ax.bar(labels, sags, color=colors, width=0.6)

        # Optimal zone lines
        ax.axhline(y=travel * 0.25, color='#4ecca3', linewidth=1, linestyle='--', alpha=0.5)
        ax.axhline(y=travel * 0.33, color='#4ecca3', linewidth=1, linestyle='--', alpha=0.5)
        ax.fill_between(range(-1, len(spring_rates) + 1), travel * 0.25, travel * 0.33,
                        alpha=0.1, color='#4ecca3')
        ax.text(len(spring_rates) - 0.5, travel * 0.29, 'Zona óptima (25-33%)',
                color='#4ecca3', fontsize=9, ha='right', va='center')

        # Sag values on bars
        for bar, s, p in zip(bars, sags, pcts):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                    f'{s:.0f}mm\n({p:.0f}%)', ha='center', va='bottom', color='#eee', fontsize=9)

        ax.set_xlabel('Tasa del muelle (por barra)')
        ax.set_ylabel('Sag (mm)')
        ax.set_title(f'Comparación de muelles — {weight}kg, {preload}mm precarga')
        ax.set_ylim(0, max(sags) * 1.3 if max(sags) > 0 else travel)

        plt.tight_layout()
        img = fig_to_base64(fig)

        return jsonify({
            'results': results,
            'image': img
        })
    except Exception as e:
        plt.close('all')
        return jsonify({'error': str(e)}), 400


@app.route('/api/animate', methods=['POST'])
def animate():
    """Genera una animación GIF de la suspensión."""
    if not current_state['suspension']:
        return jsonify({'error': 'Configura la geometría primero'}), 400

    try:
        data = request.json
        travel_min = float(data.get('travel_min', -50))
        travel_max = float(data.get('travel_max', 50))

        suspension = current_state['suspension']
        plotter = SuspensionPlotter(suspension)
        animator = SuspensionAnimator(suspension, plotter)

        anim = animator.animate_travel(
            travel_range=(travel_min, travel_max),
            num_frames=60,
            interval=50,
            repeat=False,
            show_trail=True
        )

        import tempfile
        tmp = tempfile.NamedTemporaryFile(suffix='.gif', delete=False)
        tmp.close()
        anim.save(tmp.name, writer='pillow', fps=20, dpi=80)
        plt.close('all')
        with open(tmp.name, 'rb') as f:
            img_b64 = base64.b64encode(f.read()).decode('utf-8')
        os.unlink(tmp.name)

        return jsonify({'image': img_b64})
    except Exception as e:
        plt.close('all')
        return jsonify({'error': str(e)}), 400


@app.route('/api/export', methods=['POST'])
def export_csv():
    """Exporta datos a CSV."""
    if not current_state['suspension']:
        return jsonify({'error': 'Configura la geometría primero'}), 400

    try:
        data = request.json
        travel_min = float(data.get('travel_min', -50))
        travel_max = float(data.get('travel_max', 50))
        num_points = int(data.get('num_points', 200))

        suspension = current_state['suspension']
        analyzer = LeverageAnalyzer(suspension)
        results = analyzer.analyze_travel_range(travel_min, travel_max, num_points=num_points)

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Wheel_Travel_mm', 'Shock_Travel_mm', 'Leverage_Ratio', 'Shock_Velocity_Relative'])

        for wt, st, lr, sv in zip(
            results['wheel_travel'],
            results['shock_travel'],
            results['leverage_ratio'],
            results['shock_velocity']
        ):
            writer.writerow([f"{wt:.3f}", f"{st:.3f}", f"{lr:.4f}", f"{sv:.4f}"])

        buf = io.BytesIO()
        buf.write(output.getvalue().encode('utf-8'))
        buf.seek(0)

        return send_file(buf, mimetype='text/csv', as_attachment=True, download_name='suspension_analysis.csv')
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    import os as _os
    debug = _os.environ.get('FLASK_DEBUG', '1') == '1'
    port = int(_os.environ.get('PORT', 5000))
    if debug:
        print("\n  Analizador de Suspensiones - Interfaz Web")
        print("  Abre http://localhost:5000 en tu navegador\n")
    app.run(debug=debug, host='0.0.0.0', port=port)
