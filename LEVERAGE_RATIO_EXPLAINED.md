# Leverage Ratio en Suspensiones de Motocicletas

## Definición del Leverage Ratio

El **Leverage Ratio (LR)** es la relación entre el movimiento de la rueda y el movimiento del amortiguador:

```
Leverage Ratio = Desplazamiento de la rueda / Desplazamiento del amortiguador

LR = Δ rueda / Δ shock
```

También se conoce como:
- **Motion Ratio**
- **Installation Ratio**
- **Wheel Rate Ratio**

---

## ¿Qué Expresa Este Valor?

### Interpretación Física

**Un LR de 3.0 significa:**
- Por cada **1 mm** que se comprime el amortiguador
- La rueda se desplaza **3 mm** verticalmente

**Un LR de 2.5 significa:**
- Por cada **1 mm** de compresión del shock
- La rueda se mueve **2.5 mm**

### Amplificación de Fuerzas

El leverage ratio funciona como una **palanca mecánica** invertida:

```
Fuerza en el amortiguador = Fuerza en la rueda × LR

Rigidez en la rueda (wheel rate) = Rigidez del muelle / LR²
```

**Nota importante:** La fuerza se amplifica proporcionalmente al LR, pero la rigidez percibida se reduce con el cuadrado del LR.

---

## Ejemplo Práctico Detallado

### Caso: LR = 3.0

#### Movimientos:
- Rueda sube **30 mm** → Shock se comprime **10 mm**
- Rueda baja **15 mm** → Shock se extiende **5 mm**
- Bache de **6 mm** → Shock se mueve **2 mm**

#### Fuerzas:
- Impacto de **300 N** en la rueda → **900 N** en el amortiguador (3× más)
- Impacto de **150 N** en la rueda → **450 N** en el shock
- Peso de **100 kg** sobre la rueda → **300 kg** sobre el shock

#### Rigidez (Spring Rate):
- Muelle de **100 N/mm** en el shock → **11.1 N/mm** en la rueda (100 / 3² = 100/9)
- Muelle de **80 N/mm** en el shock → **8.9 N/mm** en la rueda
- Muelle de **120 N/mm** en el shock → **13.3 N/mm** en la rueda

---

## Impacto del Leverage Ratio

### LR Alto (3.5 - 4.5)

#### ✅ Ventajas:
- **Sensibilidad superior:** Detecta y absorbe baches pequeños
- **Mejor tracción:** En terreno irregular y con muchos baches
- **Mayor confort:** Suspensión más "suave" al tacto
- **Vida útil del shock:** Menos fuerza transmitida → menos desgaste
- **Absorción de impactos grandes:** Mejor para saltos y grandes desniveles

#### ❌ Desventajas:
- **Muelles más rígidos necesarios:** Para compensar el efecto de palanca
- **Mayor recorrido del amortiguador:** Se usa más carrera del shock
- **Menos preciso en curvas rápidas:** Puede sentirse "flotante"
- **Más complejo de ajustar:** Pequeños cambios tienen gran efecto

#### Aplicaciones típicas:
- Enduro
- Motocross
- Trail riding
- Motos de rally

---

### LR Medio (2.5 - 3.5)

#### ✅ Ventajas:
- **Equilibrio óptimo:** Entre sensibilidad y control
- **Versátil:** Funciona bien en diferentes condiciones
- **Comportamiento predecible:** Fácil de entender y ajustar
- **Configuración estándar:** Repuestos y muelles más disponibles

#### Aplicaciones típicas:
- Sportbikes
- Naked bikes
- Touring
- Street bikes en general

---

### LR Bajo (2.0 - 2.5)

#### ✅ Ventajas:
- **Suspensión directa:** Respuesta inmediata y precisa
- **Mejor feedback:** Sientes claramente el asfalto
- **Precisión en curvas:** Excelente para alta velocidad en pista
- **Muelles más blandos:** Permite usar rates más bajos en el shock
- **Control superior:** En superficies lisas y predecibles

#### ❌ Desventajas:
- **Menos sensible:** Baches pequeños se notan más
- **Puede ser incómoda:** En carreteras en mal estado
- **Mayor fuerza en el shock:** Más desgaste y estrés en el amortiguador
- **Menos tracción:** En terreno irregular

#### Aplicaciones típicas:
- Supermoto
- Pista / Track day
- Competición en asfalto liso
- Motos de circuito

---

## Progresividad del Leverage Ratio

### ¿Qué es la Progresividad?

La progresividad indica cómo **cambia el LR** a medida que la suspensión se comprime:

```
Progresividad (%) = ((LR_final - LR_inicial) / LR_inicial) × 100
```

### Sistema Progresivo (LR aumenta en compresión)

**Ejemplo:**
```
Extensión:  LR = 2.8
Neutral:    LR = 3.0
Compresión: LR = 3.3
Progresividad: +17.9%
```

#### Comportamiento:
- **Inicio del recorrido:** Suave y sensible
- **Mitad del recorrido:** Equilibrado
- **Final del recorrido:** Más rígido (resiste fondeos)

#### Ventajas:
- Absorbe baches pequeños fácilmente
- Resiste impactos grandes sin fondear
- Versatilidad en diferentes condiciones
- Mejor control de la geometría de la moto

#### Ideal para:
- Enduro
- Trail
- Uso general en carretera
- Motos que deben funcionar bien en diferentes terrenos

---

### Sistema Lineal (LR aproximadamente constante)

**Ejemplo:**
```
Extensión:  LR = 2.9
Neutral:    LR = 3.0
Compresión: LR = 3.1
Progresividad: +6.9%
```

#### Comportamiento:
- **Consistente** a lo largo de todo el recorrido
- Respuesta **predecible**
- Fácil de entender y ajustar

#### Ventajas:
- Muy predecible
- Fácil de configurar
- Comportamiento homogéneo
- Menos sorpresas en condiciones variadas

#### Ideal para:
- Sportbikes
- Pista
- Riders experimentados que quieren control preciso
- Superficies consistentes (asfalto bueno)

---

### Sistema Regresivo (LR disminuye en compresión)

**Ejemplo:**
```
Extensión:  LR = 3.2
Neutral:    LR = 3.0
Compresión: LR = 2.7
Progresividad: -15.6%
```

#### Comportamiento:
- **Inicio del recorrido:** Rígido
- **Final del recorrido:** Más suave (¡contraproducente!)

#### Problemas:
- ⚠️ Poco común en suspensiones bien diseñadas
- ⚠️ Generalmente **no deseable**
- ⚠️ Puede causar sensación de "fondeo" prematuro
- ⚠️ Pérdida de control al final del recorrido
- ⚠️ Geometría de la moto se degrada en compresión

#### Cuándo puede aparecer:
- Geometrías mal diseñadas
- Anclajes del shock mal posicionados
- Sistemas con bieletas incorrectamente diseñadas

---

## Relación con el Spring Rate

### Fórmula Fundamental

```
Wheel Rate = Spring Rate del Muelle / LR²
```

**Nota:** El LR se eleva al cuadrado, lo que significa que pequeños cambios en LR tienen gran impacto.

### Ejemplo Real Detallado

**Configuración base:**
- Muelle: **80 N/mm**
- LR: **3.0**

```
Wheel Rate = 80 / (3.0)² = 80 / 9 = 8.9 N/mm
```

En la rueda se siente como un muelle de **8.9 N/mm**.

**Si cambias el LR a 2.5:**
```
Wheel Rate = 80 / (2.5)² = 80 / 6.25 = 12.8 N/mm
```

La suspensión se siente **44% más rígida** (12.8 vs 8.9) ¡con el mismo muelle!

**Si cambias el LR a 3.5:**
```
Wheel Rate = 80 / (3.5)² = 80 / 12.25 = 6.5 N/mm
```

La suspensión se siente **27% más suave** (6.5 vs 8.9).

### Tabla de Conversión

Para un muelle de **80 N/mm**:

| LR  | Wheel Rate | Variación |
|-----|------------|-----------|
| 2.0 | 20.0 N/mm  | +125%     |
| 2.5 | 12.8 N/mm  | +44%      |
| 3.0 | 8.9 N/mm   | Base      |
| 3.5 | 6.5 N/mm   | -27%      |
| 4.0 | 5.0 N/mm   | -44%      |
| 4.5 | 3.9 N/mm   | -56%      |

---

## Cómo Usar el Programa de Análisis

### Funcionalidades del Programa

Tu programa calcula automáticamente:

1. **LR instantáneo** en cualquier posición del recorrido
2. **LR promedio** a lo largo de todo el recorrido
3. **LR máximo y mínimo** del sistema
4. **Progresividad** (porcentaje de cambio del LR)
5. **Clasificación** (progresivo/lineal/regresivo)
6. **Curvas gráficas** de LR vs desplazamiento
7. **Relación** wheel travel vs shock travel

### Interpretación de Resultados

**Ejemplo de salida del programa:**

```
Leverage Ratio inicial (neutral):  2.85
Leverage Ratio promedio:           2.92
Leverage Ratio máximo:             3.15
Leverage Ratio mínimo:             2.68

Progresividad:                     10.5%
Tipo de sistema:                   PROGRESIVO
```

**Interpretación:**
- Sistema con LR medio-alto (2.92)
- Suspensión sensible pero controlada
- 10.5% progresivo = buen equilibrio
- Se endurece moderadamente en compresión
- Ideal para sportbike o uso mixto

### Optimización

**Para aumentar el LR:**
- Mover el anclaje del shock en el basculante más cerca del eje de rueda
- Subir el anclaje del shock en el chasis
- Aumentar el ángulo del basculante

**Para disminuir el LR:**
- Mover el anclaje del shock en el basculante más cerca del pivote
- Bajar el anclaje del shock en el chasis
- Disminuir el ángulo del basculante

**Para aumentar la progresividad:**
- Los cambios dependen de la geometría específica
- Usar el programa para probar diferentes configuraciones
- Buscar que el LR aumente ~10-20% del inicio al final del recorrido

---

## Valores Típicos por Categoría

### Tabla de Referencia

| Categoría           | LR Típico | Progresividad | Características                    |
|---------------------|-----------|---------------|------------------------------------|
| **Motocross**       | 3.5-4.5   | +20% a +40%   | Muy progresivo, gran sensibilidad  |
| **Enduro**          | 3.0-4.0   | +15% a +30%   | Progresivo, versátil               |
| **Trail**           | 2.8-3.5   | +10% a +25%   | Moderadamente progresivo           |
| **Sportbike**       | 2.5-3.2   | +5% a +15%    | Ligeramente progresivo             |
| **Supermoto**       | 2.3-2.8   | 0% a +10%     | Lineal o poco progresivo           |
| **Touring**         | 2.7-3.3   | +8% a +18%    | Progresivo para confort            |
| **MotoGP**          | 2.6-3.0   | +5% a +12%    | Optimizado, ligeramente progresivo |
| **Pista (track)**   | 2.4-2.9   | 0% a +8%      | Lineal, muy predecible             |

### Notas por Categoría

**Motocross/Enduro:**
- Necesitan alta sensibilidad para terreno irregular
- Progresividad alta para resistir fondeos en saltos
- LR alto permite usar muelles duros sin perder sensibilidad

**Sportbike:**
- Balance entre confort y control
- Suficiente sensibilidad para carreteras imperfectas
- Suficiente precisión para conducción deportiva

**Supermoto/Pista:**
- Prioridad en precisión y feedback
- Superficies lisas permiten LR bajo
- Comportamiento lineal para predecibilidad

**MotoGP:**
- Optimización extrema para circuitos específicos
- Balance perfecto para máximo agarre
- Ajustable para diferentes pistas

---

## Factores que Afectan el Leverage Ratio

### Geometría del Basculante

1. **Longitud del basculante:**
   - Basculante más largo → cambios más suaves en LR
   - Basculante más corto → cambios más pronunciados en LR

2. **Ángulo del basculante:**
   - Mayor ángulo inicial → LR generalmente más alto
   - Afecta la progresividad del sistema

3. **Posición del anclaje del shock en el basculante:**
   - Más cerca del pivote → LR más bajo, menos progresivo
   - Más cerca de la rueda → LR más alto, más progresivo
   - Altura del anclaje afecta la curva de progresividad

### Geometría del Chasis

1. **Posición del anclaje del shock en el chasis:**
   - Más alto → LR más alto
   - Más bajo → LR más bajo
   - Posición horizontal también afecta

2. **Sistemas de bieletas:**
   - Permiten curvas de LR muy personalizadas
   - Pueden lograr progresividad muy alta
   - Más complejos de diseñar y optimizar

---

## Efectos Secundarios del Leverage Ratio

### Sobre la Geometría de la Moto

**Anti-Squat:**
- LR afecta el anti-squat bajo aceleración
- LR más alto generalmente reduce el squat
- Importante en motos de competición

**Anti-Dive:**
- Similar al anti-squat pero en frenada
- LR de la horquilla delantera afecta el dive
- Crítico para estabilidad en frenadas fuertes

### Sobre el Amortiguador

**Velocidad del pistón:**
```
Velocidad shock = Velocidad rueda / LR
```

- LR alto → pistón más lento → ajustes de compresión diferentes
- LR bajo → pistón más rápido → necesita amortiguación más fuerte

**Carrera necesaria:**
```
Carrera shock = Recorrido rueda / LR promedio
```

- LR alto → menos carrera de shock necesaria
- LR bajo → más carrera de shock necesaria

---

## Diseño y Optimización

### Proceso de Diseño Óptimo

1. **Definir requisitos:**
   - Tipo de moto y uso
   - Prioridades (confort vs control)
   - Terreno típico

2. **Establecer LR objetivo:**
   - Usar tabla de referencia
   - Considerar peso del piloto
   - Analizar competencia

3. **Diseñar geometría:**
   - Posiciones de anclajes
   - Longitud del basculante
   - Usar el programa para iterar

4. **Analizar progresividad:**
   - Verificar curva de LR
   - Ajustar para objetivo deseado
   - Comparar con motos similares

5. **Validar:**
   - Calcular wheel rates
   - Verificar carrera del shock
   - Simular casos extremos

### Errores Comunes a Evitar

❌ **LR demasiado alto:**
- Suspensión "flotante"
- Muelles extremadamente duros
- Difícil de ajustar

❌ **LR demasiado bajo:**
- Suspensión muy dura
- Poca sensibilidad
- Alto desgaste del shock

❌ **Sistema regresivo:**
- Comportamiento impredecible
- Fondeos inesperados
- Pérdida de control

❌ **Progresividad excesiva:**
- Comportamiento inconsistente
- Difícil de configurar
- Cambios bruscos en el comportamiento

---

## Resumen Ejecutivo

### El Leverage Ratio determina:

| Aspecto                  | Impacto                                      |
|--------------------------|----------------------------------------------|
| 📏 **Movimientos**       | Cuánto se mueve la rueda vs el shock         |
| 💪 **Fuerzas**          | Cuánta fuerza llega al amortiguador          |
| 🔧 **Rigidez**          | Qué spring rate necesitas                    |
| 🏍️ **Sensación**       | Cómo se sentirá la moto al rodar             |
| 📊 **Progresividad**    | Cómo cambia el comportamiento en compresión  |
| ⚙️ **Ajustes**          | Complejidad de configuración y ajuste        |

### Regla General

```
LR más alto  →  Suspensión más sensible + Muelles más duros
LR más bajo  →  Suspensión más directa + Muelles más blandos
```

### Por Qué Este Programa es Útil

El programa de análisis de cinemática te permite:

1. **Diseñar** el leverage ratio óptimo para tu aplicación
2. **Optimizar** la progresividad del sistema
3. **Predecir** el comportamiento antes de fabricar
4. **Comparar** diferentes configuraciones fácilmente
5. **Calcular** spring rates necesarios con precisión
6. **Entender** cómo cambios geométricos afectan el LR
7. **Documentar** y compartir diseños con el equipo

---

## Referencias y Lecturas Adicionales

### Conceptos Relacionados

- **Wheel Rate:** Rigidez efectiva percibida en la rueda
- **Spring Rate:** Rigidez del muelle del amortiguador
- **Anti-Squat:** Resistencia al hundimiento en aceleración
- **Anti-Dive:** Resistencia al hundimiento en frenada
- **Rising Rate:** Otro término para sistemas progresivos
- **Falling Rate:** Otro término para sistemas regresivos (indeseables)

### Herramientas

Este programa calcula todo automáticamente. Úsalo para:
- Diseño inicial
- Optimización iterativa
- Comparación de alternativas
- Documentación de decisiones de diseño
- Formación del equipo en cinemática de suspensiones

---

**Documento creado para el proyecto de análisis de cinemática de suspensiones - Equipo MotorStudent**
