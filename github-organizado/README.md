# Estimador de Costos de Reparación de Tuberías

## Descripción
Herramienta web y scripts para estimar costos de reparación de tuberías usando productos DEACON Rocket.

## Estructura del repositorio

- `src/web/` — Aplicación web (HTML, JS, CSS)
- `src/scripts/` — Scripts de utilidad general (Python, JS)
- `src/ingenieria/` — Cálculos, visualización y simulación en ingeniería mecánica
- `src/analisis/` — Análisis financiero y de operaciones
- `src/estadistica/` — Estadística y análisis de datos
- `src/mantenimiento/` — Gestión y control de mantenimiento
- `src/gui/` — Aplicaciones gráficas interactivas (Tkinter, etc.)
- `docs/` — Manuales, explicaciones y ejemplos
- `assets/` — Imágenes y recursos gráficos
- `data/` — Archivos de datos de ejemplo
- `tests/` — Pruebas y ejemplos de uso

## Clasificación y utilidad de los scripts en Ingeniería Mecánica

### 1. Cálculo y simulación de sistemas mecánicos
- `src/ingenieria/CURVA_BOMBA.py`, `CURVA_BOMBA_2.py`, `CURVA2.py`, `curva_mtto.py`, `sfd1.py`:
  - Permiten calcular curvas de operación de bombas, sistemas de tuberías y análisis de esfuerzos.
  - Útiles para el diseño, selección y mantenimiento de equipos hidráulicos.
- `src/ingenieria/RUNGE_KUTTA.py`:
  - Implementa métodos numéricos para resolver ecuaciones diferenciales aplicadas a sistemas dinámicos.

### 2. Visualización y análisis de datos
- `src/ingenieria/Grafica_Duran.py`, `Grafica_duran_1.py`, `Graph_durant.py`:
  - Scripts para graficar resultados de simulaciones, tendencias de operación y análisis de datos experimentales.

### 3. Estadística aplicada
- `src/estadistica/ESTADISTICA.py`:
  - Herramientas para análisis estadístico de datos de operación, fallas y mantenimiento.

### 4. Análisis financiero y de operaciones
- `src/analisis/Analisis.py`, `Analisis_1.py`, `Opex_2025.py`, `Requerimiento_mes.py`:
  - Permiten evaluar costos, proyecciones y requerimientos de recursos en proyectos de ingeniería.

### 5. Gestión de mantenimiento
- `src/mantenimiento/gestion_mtto.py`:
  - Automatiza y controla actividades de mantenimiento preventivo y correctivo.

### 6. Aplicaciones gráficas interactivas
- `src/gui/MODELO_GRUA.py`:
  - Simulación y estudio de planes de izaje seguro con grúas, integrando cálculos, visualización y cuestionarios.

### 7. Utilidades generales
- `src/scripts/`:
  - Scripts de apoyo para cálculos, conversiones y automatización de tareas repetitivas.

## Resumen de utilidad en Ingeniería Mecánica

Esta colección de scripts y aplicaciones permite:
- Realizar cálculos hidráulicos, estructurales y de operación de equipos.
- Simular y visualizar el comportamiento de sistemas mecánicos.
- Analizar datos experimentales y de operación para la toma de decisiones.
- Optimizar el mantenimiento y la gestión de recursos.
- Evaluar costos y proyecciones económicas en proyectos.
- Mejorar la seguridad y la formación mediante simuladores y herramientas interactivas.

Todo esto contribuye a una ingeniería mecánica más eficiente, segura y basada en datos.

## Uso rápido

1. Abre `src/web/CALCULO TUBERIAS.html` en tu navegador.
2. Consulta `docs/` para manuales y ejemplos.
3. Usa los scripts de las carpetas según tu necesidad y especialidad.

## Licencia
[MIT](LICENSE)
