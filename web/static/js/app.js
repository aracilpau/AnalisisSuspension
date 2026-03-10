// ============ NAVIGATION ============

// Landing -> Study
document.querySelectorAll('.study-card[data-study]').forEach(card => {
    card.addEventListener('click', () => {
        document.getElementById('landing').classList.remove('active');
        document.getElementById('study-' + card.dataset.study).classList.add('active');
    });
});

// Back buttons
document.querySelectorAll('.btn-back').forEach(btn => {
    btn.addEventListener('click', () => {
        btn.closest('.view').classList.remove('active');
        document.getElementById('landing').classList.add('active');
    });
});

// Tab navigation (works for all studies)
document.querySelectorAll('.tabs').forEach(tabBar => {
    tabBar.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const parent = tab.closest('.view');
            parent.querySelectorAll('.tabs .tab').forEach(t => t.classList.remove('active'));
            parent.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById(tab.dataset.section).classList.add('active');
        });
    });
});

// ============ LEVERAGE RATIO STUDY ============

let leverageConfigured = false;

async function loadPresets(gridId, prefix) {
    const res = await fetch('/api/presets');
    const presets = await res.json();
    const grid = document.getElementById(gridId);

    grid.innerHTML = Object.entries(presets).map(([key, p]) =>
        `<button class="preset-btn" data-preset="${key}">
            <span class="preset-name">${p.name}</span>
            <span class="preset-desc">${p.desc}</span>
        </button>`
    ).join('');

    grid.innerHTML += `<button class="preset-btn" data-preset="custom">
        <span class="preset-name">Personalizada</span>
        <span class="preset-desc">Valores manuales</span>
    </button>`;

    grid.querySelectorAll('.preset-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            grid.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            if (btn.dataset.preset !== 'custom') {
                const res = await fetch('/api/preset/' + btn.dataset.preset);
                const vals = await res.json();
                document.getElementById(prefix + 'swingarm_length').value = vals.swingarm_length;
                document.getElementById(prefix + 'swingarm_angle').value = vals.swingarm_angle;
                document.getElementById(prefix + 'shock_sw_x').value = vals.shock_sw_x;
                document.getElementById(prefix + 'shock_sw_y').value = vals.shock_sw_y;
                document.getElementById(prefix + 'shock_ch_x').value = vals.shock_ch_x;
                document.getElementById(prefix + 'shock_ch_y').value = vals.shock_ch_y;
                document.getElementById(prefix + 'wheel_radius').value = vals.wheel_radius;
            }
        });
    });
}

function getGeometryParams(prefix) {
    return {
        swingarm_length: document.getElementById(prefix + 'swingarm_length').value,
        swingarm_angle: document.getElementById(prefix + 'swingarm_angle').value,
        shock_sw_x: document.getElementById(prefix + 'shock_sw_x').value,
        shock_sw_y: document.getElementById(prefix + 'shock_sw_y').value,
        shock_ch_x: document.getElementById(prefix + 'shock_ch_x').value,
        shock_ch_y: document.getElementById(prefix + 'shock_ch_y').value,
        wheel_radius: document.getElementById(prefix + 'wheel_radius').value
    };
}

// Configure leverage suspension
document.getElementById('btn-configure').addEventListener('click', async () => {
    const btn = document.getElementById('btn-configure');
    const result = document.getElementById('config-result');
    btn.disabled = true;
    btn.textContent = 'Configurando...';

    const activePreset = document.querySelector('#preset-grid .preset-btn.active');
    const presetName = activePreset ? activePreset.querySelector('.preset-name').textContent : 'Personalizada';

    try {
        const params = getGeometryParams('');
        params.preset_name = presetName;
        const res = await fetch('/api/configure', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params)
        });
        const data = await res.json();
        if (data.success) {
            leverageConfigured = true;
            result.className = 'result-message success';
            result.textContent = `${data.message} — Longitud shock: ${data.shock_length} mm`;
            document.getElementById('lev-status-badge').textContent = presetName;
            document.getElementById('lev-status-badge').classList.add('configured');
            loadSummary();
            document.getElementById('stroke-card').style.display = 'block';
        } else {
            result.className = 'result-message error';
            result.textContent = 'Error: ' + data.error;
        }
    } catch (e) {
        result.className = 'result-message error';
        result.textContent = 'Error de conexión';
    }
    btn.disabled = false;
    btn.textContent = 'Configurar Suspensión';
});

async function loadSummary() {
    try {
        const res = await fetch('/api/summary');
        const data = await res.json();
        document.getElementById('summary-content').innerHTML = `
            <div>
                <div class="summary-item"><span class="label">Basculante</span><span class="value">${data.swingarm_length} mm</span></div>
                <div class="summary-item"><span class="label">Ángulo</span><span class="value">${data.swingarm_angle}°</span></div>
                <div class="summary-item"><span class="label">Radio rueda</span><span class="value">${data.wheel_radius} mm</span></div>
            </div>
            <div>
                <div class="summary-item"><span class="label">Long. shock</span><span class="value">${data.initial_shock_length} mm</span></div>
                <div class="summary-item"><span class="label">LR (neutral)</span><span class="value">${data.lr_neutral}</span></div>
                <div class="summary-item"><span class="label">Progresividad</span><span class="value">${data.progression}%</span></div>
                <div class="summary-item"><span class="label">Tipo</span><span class="value">${data.system_type.toUpperCase()}</span></div>
            </div>`;
        document.getElementById('summary-card').style.display = 'block';
    } catch (e) { console.error(e); }
}

// Stroke to wheel travel
let calculatedWheelTravel = null;

document.getElementById('btn-stroke-calc').addEventListener('click', async () => {
    if (!leverageConfigured) return;
    try {
        const res = await fetch('/api/shock_to_wheel', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ shock_stroke: document.getElementById('shock-stroke').value })
        });
        const data = await res.json();
        if (data.error) { alert(data.error); return; }

        calculatedWheelTravel = data.wheel_travel;

        document.getElementById('stroke-shock-val').textContent = data.shock_stroke + ' mm';
        document.getElementById('stroke-wheel-val').textContent = data.wheel_travel + ' mm';
        document.getElementById('stroke-lr-val').textContent = data.lr_average;
        document.getElementById('stroke-hint').textContent =
            `Con ${data.shock_stroke}mm de stroke y un LR medio de ${data.lr_average}, tu rueda recorre ${data.wheel_travel}mm. Este valor se ha aplicado automáticamente a los análisis.`;
        document.getElementById('stroke-results').style.display = 'block';

        // Auto-fill analysis fields
        document.getElementById('analyze-max').value = data.wheel_travel;
        document.getElementById('anim-max').value = data.wheel_travel;
        document.getElementById('export-max').value = data.wheel_travel;
        document.getElementById('viz-displacement').value = Math.round(data.wheel_travel / 2);
    } catch (e) { alert('Error de conexión'); }
});

function checkLeverageConfigured() {
    if (!leverageConfigured) {
        alert('Primero configura la geometría en la pestaña "Geometría"');
        return false;
    }
    return true;
}

// Visualize
document.getElementById('btn-visualize').addEventListener('click', async () => {
    if (!checkLeverageConfigured()) return;
    const plot = document.getElementById('viz-plot');
    plot.innerHTML = '<div class="loading">Generando visualización...</div>';
    try {
        const res = await fetch('/api/visualize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ wheel_displacement: document.getElementById('viz-displacement').value })
        });
        const data = await res.json();
        plot.innerHTML = data.error
            ? `<div class="loading" style="color:var(--accent)">${data.error}</div>`
            : `<img src="data:image/png;base64,${data.image}" alt="Geometría">`;
    } catch (e) {
        plot.innerHTML = '<div class="loading" style="color:var(--accent)">Error de conexión</div>';
    }
});

// Animate
document.getElementById('btn-animate').addEventListener('click', async () => {
    if (!checkLeverageConfigured()) return;
    const plot = document.getElementById('anim-plot');
    plot.innerHTML = '<div class="loading">Generando animación (puede tardar unos segundos)...</div>';
    try {
        const res = await fetch('/api/animate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                travel_min: document.getElementById('anim-min').value,
                travel_max: document.getElementById('anim-max').value
            })
        });
        const data = await res.json();
        plot.innerHTML = data.error
            ? `<div class="loading" style="color:var(--accent)">${data.error}</div>`
            : `<img src="data:image/gif;base64,${data.image}" alt="Animación">`;
    } catch (e) {
        plot.innerHTML = '<div class="loading" style="color:var(--accent)">Error de conexión</div>';
    }
});

// Analyze
document.getElementById('btn-analyze').addEventListener('click', async () => {
    if (!checkLeverageConfigured()) return;
    const plot = document.getElementById('analyze-plot');
    plot.innerHTML = '<div class="loading">Analizando...</div>';
    try {
        const res = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                travel_min: document.getElementById('analyze-min').value,
                travel_max: document.getElementById('analyze-max').value
            })
        });
        const data = await res.json();
        if (data.error) {
            plot.innerHTML = `<div class="loading" style="color:var(--accent)">${data.error}</div>`;
            return;
        }
        document.getElementById('lr-initial').textContent = data.lr_initial;
        document.getElementById('lr-average').textContent = data.lr_average;
        document.getElementById('lr-max').textContent = data.lr_max;
        document.getElementById('lr-min').textContent = data.lr_min;
        document.getElementById('lr-progression').textContent = data.progression + '%';
        const typeEl = document.getElementById('lr-type');
        typeEl.textContent = data.system_type.toUpperCase();
        typeEl.className = 'stat-value type-' + data.system_type;
        document.getElementById('analyze-results').style.display = 'block';
        plot.innerHTML = `<img src="data:image/png;base64,${data.image}" alt="Leverage Ratio">`;
    } catch (e) {
        plot.innerHTML = '<div class="loading" style="color:var(--accent)">Error de conexión</div>';
    }
});

// Calculate LR
document.getElementById('btn-calculate').addEventListener('click', async () => {
    if (!checkLeverageConfigured()) return;
    try {
        const res = await fetch('/api/leverage', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ wheel_displacement: document.getElementById('calc-displacement').value })
        });
        const data = await res.json();
        if (data.error) { alert(data.error); return; }
        document.getElementById('calc-wheel').textContent = data.wheel_displacement + ' mm';
        document.getElementById('calc-shock').textContent = data.shock_travel + ' mm';
        document.getElementById('calc-lr').textContent = data.leverage_ratio;
        document.getElementById('calc-shock-len').textContent = data.shock_length + ' mm';
        document.getElementById('calc-initial-len').textContent = data.initial_shock_length + ' mm';
        document.getElementById('calc-results').style.display = 'block';
    } catch (e) { alert('Error de conexión'); }
});

// Export CSV
document.getElementById('btn-export').addEventListener('click', async () => {
    if (!checkLeverageConfigured()) return;
    try {
        const res = await fetch('/api/export', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                travel_min: document.getElementById('export-min').value,
                travel_max: document.getElementById('export-max').value,
                num_points: document.getElementById('export-points').value
            })
        });
        if (!res.ok) { const err = await res.json(); alert(err.error); return; }
        const blob = await res.blob();
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'suspension_analysis.csv';
        a.click();
    } catch (e) { alert('Error de conexión'); }
});

// ============ SAG CALCULATOR ============

document.getElementById('btn-sag-calculate').addEventListener('click', async () => {
    const btn = document.getElementById('btn-sag-calculate');
    const result = document.getElementById('sag-config-result');
    btn.disabled = true;
    btn.textContent = 'Calculando...';

    try {
        // First calculate wheel travel from shock stroke
        const geoParams = getGeometryParams('sag-');
        const configRes = await fetch('/api/configure', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ...geoParams, preset_name: 'Sag' })
        });
        const configData = await configRes.json();
        if (!configData.success) { throw new Error(configData.error); }

        const strokeRes = await fetch('/api/shock_to_wheel', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ shock_stroke: document.getElementById('sag-shock_stroke').value })
        });
        const strokeData = await strokeRes.json();
        if (!strokeData.error) {
            document.getElementById('sag-max_travel').value = strokeData.wheel_travel;
        }

        const params = getGeometryParams('sag-');
        params.spring_rate = document.getElementById('sag-spring_rate').value;
        params.preload = document.getElementById('sag-preload').value;
        params.weight = document.getElementById('sag-weight').value;
        params.max_travel = document.getElementById('sag-max_travel').value;

        const res = await fetch('/api/sag', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params)
        });
        const data = await res.json();

        if (data.error) {
            result.className = 'result-message error';
            result.textContent = 'Error: ' + data.error;
        } else {
            result.className = 'result-message success';
            result.textContent = 'Sag calculado correctamente';
            document.getElementById('sag-status-badge').textContent = 'Calculado';
            document.getElementById('sag-status-badge').classList.add('configured');
            showSagResults(data);

            // Switch to results tab
            const parent = document.getElementById('study-sag');
            parent.querySelectorAll('.tabs .tab').forEach(t => t.classList.remove('active'));
            parent.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
            parent.querySelector('[data-section="sag-results"]').classList.add('active');
            document.getElementById('sag-results').classList.add('active');
        }
    } catch (e) {
        result.className = 'result-message error';
        result.textContent = 'Error de conexión';
    }

    btn.disabled = false;
    btn.textContent = 'Calcular Sag';
});

function showSagResults(data) {
    const content = document.getElementById('sag-results-content');
    const pctClass = data.sag_percent >= 25 && data.sag_percent <= 33
        ? 'type-progresivo'
        : data.sag_percent < 25 ? 'type-regresivo' : 'type-lineal';

    let verdict = '';
    if (data.sag_percent < 5) verdict = 'Muelle demasiado duro o mucha precarga. La suspensión apenas trabaja.';
    else if (data.sag_percent < 20) verdict = 'Sag bajo. Bueno para free sag, pero si es rider sag necesitas menos precarga o muelle más blando.';
    else if (data.sag_percent <= 33) verdict = 'Sag en rango óptimo para rider sag. Buen setup.';
    else if (data.sag_percent <= 40) verdict = 'Sag algo alto. Considera más precarga o muelle más duro.';
    else verdict = 'Sag excesivo. Muelle demasiado blando. Riesgo de tocar fondo.';

    content.innerHTML = `
        <div class="stat-grid">
            <div class="stat-card">
                <span class="stat-label">Sag Rueda</span>
                <span class="stat-value">${data.wheel_sag} mm</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">Sag Shock</span>
                <span class="stat-value">${data.shock_sag} mm</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">% del Recorrido</span>
                <span class="stat-value ${pctClass}">${data.sag_percent}%</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">LR en Sag</span>
                <span class="stat-value">${data.lr_at_sag}</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">Fuerza Muelle</span>
                <span class="stat-value">${data.spring_force} N</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">Fuerza Rueda</span>
                <span class="stat-value">${data.wheel_force} N</span>
            </div>
        </div>
        <div class="card" style="margin-top:16px;border-left:3px solid var(--accent)">
            <p><strong>Valoración:</strong> ${verdict}</p>
        </div>
    `;

    // Show plot if available
    if (data.image) {
        document.getElementById('sag-plot').innerHTML = `<img src="data:image/png;base64,${data.image}" alt="Sag">`;
    }
}

// ============ FRONT FORK STUDY ============

document.getElementById('btn-fork-calculate').addEventListener('click', async () => {
    const btn = document.getElementById('btn-fork-calculate');
    const result = document.getElementById('fork-config-result');
    btn.disabled = true;
    btn.textContent = 'Calculando...';

    try {
        const kNmm = parseFloat(document.getElementById('fork-spring_rate').value);
        const res = await fetch('/api/fork_sag', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                travel: document.getElementById('fork-travel').value,
                spring_rate: kNmm,
                preload: document.getElementById('fork-preload').value,
                weight: document.getElementById('fork-weight').value
            })
        });
        const data = await res.json();

        if (data.error) {
            result.className = 'result-message error';
            result.textContent = 'Error: ' + data.error;
        } else {
            result.className = 'result-message success';
            result.textContent = 'Sag calculado correctamente';
            showForkResults(data);
        }
    } catch (e) {
        result.className = 'result-message error';
        result.textContent = 'Error de conexión';
    }

    btn.disabled = false;
    btn.textContent = 'Calcular Sag Delantero';
});

function showForkResults(data) {
    const container = document.getElementById('fork-results-content');
    container.style.display = 'block';

    const pctClass = data.sag_percent >= 25 && data.sag_percent <= 33
        ? 'type-progresivo'
        : data.sag_percent < 25 ? 'type-regresivo' : 'type-lineal';

    let verdict = '';
    if (data.sag_percent < 1) verdict = 'Precarga excesiva. El muelle no se comprime con este peso. Reduce la precarga o baja de muelle.';
    else if (data.sag_percent < 20) verdict = 'Sag bajo. Muelle muy duro o mucha precarga. Si es rider sag, baja de muelle.';
    else if (data.sag_percent <= 33) verdict = 'Sag en rango óptimo (25-33%). Buen setup para la horquilla.';
    else if (data.sag_percent <= 40) verdict = 'Sag algo alto. Considera más precarga o subir de muelle.';
    else verdict = 'Sag excesivo. Muelle demasiado blando. Riesgo de tocar fondo en frenada. Sube de muelle.';

    container.innerHTML = `
        <div class="card" style="margin-top:16px">
            <div class="stat-grid">
                <div class="stat-card">
                    <span class="stat-label">Sag</span>
                    <span class="stat-value">${data.sag} mm</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">% del Recorrido</span>
                    <span class="stat-value ${pctClass}">${data.sag_percent}%</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">Fuerza muelles</span>
                    <span class="stat-value">${data.spring_force} N</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">Peso</span>
                    <span class="stat-value">${data.weight_force} N</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">Tasa total (2×)</span>
                    <span class="stat-value">${data.total_rate} N/mm</span>
                    <span class="stat-label">${(data.total_rate / 2).toFixed(2)} N/mm × 2</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">Recorrido libre</span>
                    <span class="stat-value">${data.travel - data.sag} mm</span>
                </div>
            </div>
            <div class="card" style="margin-top:16px;border-left:3px solid var(--accent)">
                <p><strong>Valoración:</strong> ${verdict}</p>
            </div>
            <div id="fork-plot" class="plot-container" style="margin-top:16px"></div>
        </div>
    `;

    if (data.image) {
        document.getElementById('fork-plot').innerHTML = `<img src="data:image/png;base64,${data.image}" alt="Fork Sag">`;
    }
}

// Fork compare all springs
document.getElementById('btn-fork-compare').addEventListener('click', async () => {
    const btn = document.getElementById('btn-fork-compare');
    const container = document.getElementById('fork-compare-results');
    btn.disabled = true;
    btn.textContent = 'Comparando...';
    container.innerHTML = '<div class="loading">Calculando todos los muelles...</div>';

    try {
        const res = await fetch('/api/fork_compare', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                weight: document.getElementById('fork-compare-weight').value,
                preload: document.getElementById('fork-compare-preload').value,
                travel: document.getElementById('fork-compare-travel').value
            })
        });
        const data = await res.json();

        if (data.error) {
            container.innerHTML = `<div class="result-message error">${data.error}</div>`;
        } else {
            let html = '<div class="stat-grid" style="margin-top:16px">';
            data.results.forEach(r => {
                const pctClass = r.sag_percent >= 25 && r.sag_percent <= 33
                    ? 'type-progresivo'
                    : r.sag_percent < 25 ? 'type-regresivo' : 'type-lineal';
                const tag = r.sag_percent >= 25 && r.sag_percent <= 33
                    ? '<span style="color:var(--green);font-size:12px">✓ Óptimo</span>'
                    : r.sag_percent < 25
                        ? '<span style="color:var(--accent);font-size:12px">Duro</span>'
                        : '<span style="color:var(--accent);font-size:12px">Blando</span>';
                html += `
                    <div class="stat-card">
                        <span class="stat-label">${r.spring_rate_nmm} N/mm × 2</span>
                        <span class="stat-value ${pctClass}">${r.sag} mm</span>
                        <span class="stat-label">${r.sag_percent}% — ${tag}</span>
                    </div>`;
            });
            html += '</div>';

            if (data.image) {
                html += `<div class="plot-container" style="margin-top:16px"><img src="data:image/png;base64,${data.image}" alt="Comparación"></div>`;
            }

            container.innerHTML = html;
        }
    } catch (e) {
        container.innerHTML = '<div class="result-message error">Error de conexión</div>';
    }

    btn.disabled = false;
    btn.textContent = 'Comparar';
});

// ============ PALETTES ============

const PALETTES = [
    {
        id: 'default', name: 'Crimson',
        bg: '#0f0f1a', surface: '#1a1a2e', surface2: '#252542',
        accent: '#e94560', text: '#eaeaea', textMuted: '#8888aa',
        green: '#4ecca3', yellow: '#ffc947'
    },
    {
        id: 'carbon', name: 'Carbon',
        bg: '#0F0F0F', surface: '#1E1E1E', surface2: '#2E2E2E',
        accent: '#2E75B6', text: '#E8E8E8', textMuted: '#9E9E9E',
        green: '#00C896', yellow: '#ffc947'
    },
    {
        id: 'midnight', name: 'Midnight',
        bg: '#0A0E1A', surface: '#131929', surface2: '#1E2840',
        accent: '#4A90D9', text: '#F0F4FF', textMuted: '#8899BB',
        green: '#4ecca3', yellow: '#FF6B35'
    },
    {
        id: 'github', name: 'GitHub Dark',
        bg: '#111318', surface: '#1C2128', surface2: '#2D333B',
        accent: '#58A6FF', text: '#CDD9E5', textMuted: '#768390',
        green: '#3FB950', yellow: '#D29922'
    },
    {
        id: 'amber', name: 'Amber',
        bg: '#1A1A1A', surface: '#2D2D2D', surface2: '#3D3D3D',
        accent: '#E8A020', text: '#F5F5F5', textMuted: '#AAAAAA',
        green: '#4ecca3', yellow: '#E8A020'
    },
    {
        id: 'light', name: 'Light',
        bg: '#F8F9FA', surface: '#EAEDF0', surface2: '#D5DAE0',
        accent: '#1F5C8B', text: '#1A1A2E', textMuted: '#555E6B',
        green: '#0077CC', yellow: '#D97706'
    }
];

function applyPalette(palette) {
    const r = document.documentElement.style;
    r.setProperty('--bg', palette.bg);
    r.setProperty('--surface', palette.surface);
    r.setProperty('--surface2', palette.surface2);
    r.setProperty('--accent', palette.accent);
    r.setProperty('--text', palette.text);
    r.setProperty('--text-muted', palette.textMuted);
    r.setProperty('--green', palette.green);
    r.setProperty('--yellow', palette.yellow);
    localStorage.setItem('isc-palette', palette.id);

    document.querySelectorAll('.palette-option').forEach(o => {
        o.classList.toggle('active', o.dataset.palette === palette.id);
    });
}

function initPalettes() {
    const list = document.getElementById('palette-list');
    list.innerHTML = PALETTES.map(p =>
        `<button class="palette-option" data-palette="${p.id}">
            <div class="palette-swatches">
                <div class="palette-swatch" style="background:${p.bg}"></div>
                <div class="palette-swatch" style="background:${p.surface}"></div>
                <div class="palette-swatch" style="background:${p.accent}"></div>
                <div class="palette-swatch" style="background:${p.green}"></div>
            </div>
            <span class="palette-option-name">${p.name}</span>
        </button>`
    ).join('');

    list.querySelectorAll('.palette-option').forEach(btn => {
        btn.addEventListener('click', () => {
            const p = PALETTES.find(p => p.id === btn.dataset.palette);
            if (p) applyPalette(p);
        });
    });

    // Load saved palette
    const saved = localStorage.getItem('isc-palette');
    const palette = PALETTES.find(p => p.id === saved) || PALETTES[0];
    applyPalette(palette);

    // Toggle dropdown
    document.getElementById('btn-palette').addEventListener('click', (e) => {
        e.stopPropagation();
        document.getElementById('palette-dropdown').classList.toggle('hidden');
    });

    document.addEventListener('click', (e) => {
        const dd = document.getElementById('palette-dropdown');
        if (!dd.contains(e.target) && e.target !== document.getElementById('btn-palette')) {
            dd.classList.add('hidden');
        }
    });
}

// ============ INIT ============
loadPresets('preset-grid', '');
loadPresets('sag-preset-grid', 'sag-');
initPalettes();
