# Capítulo 10: Transformadas de Fourier

Este capítulo introduce las Transformadas de Fourier, una herramienta matemática indispensable en ingeniería para analizar señales y funciones en el dominio de la frecuencia. Nos permite descomponer una señal compleja en sus componentes de frecuencia individuales, revelando información que no es obvia en el dominio del tiempo.

## Contenido Teórico

La Transformada de Fourier es fundamental en el procesamiento de señales, el análisis de vibraciones, el control de sistemas, la óptica y muchas otras áreas. La idea central es que cualquier señal periódica (o no periódica, bajo ciertas condiciones) puede representarse como una suma de senos y cosenos de diferentes frecuencias y amplitudes.

*   **Dominio del Tiempo vs. Dominio de la Frecuencia:** Una señal puede verse cómo cambia con el tiempo (dominio del tiempo) o qué frecuencias la componen (dominio de la frecuencia).
*   **Serie de Fourier:** Para señales periódicas, las Series de Fourier las descomponen en una suma de armónicos.
*   **Transformada de Fourier Continua:** Extiende el concepto a señales no periódicas.
*   **Transformada Discreta de Fourier (DFT):** Para señales discretas (muestreadas), como las obtenidas de sensores. Convierte una secuencia finita de muestras en una secuencia finita de componentes de frecuencia.
*   **Transformada Rápida de Fourier (FFT):** Un algoritmo eficiente para calcular la DFT. Es la base de casi todo el análisis de frecuencia digital.

## Ejercicios Prácticos

Cada ejercicio es un script de Python (`.py`) con comentarios detallados y ejemplos relevantes para la ingeniería.

### `ejercicio_1_introduccion_senales.py`

*   **Descripción:** Introduce el concepto de señales en el dominio del tiempo y cómo se componen de diferentes frecuencias. Se visualizan señales simples (senos y cosenos) y una señal compuesta por la suma de varias frecuencias.
*   **Conceptos Clave:** Señal, frecuencia, amplitud, fase, superposición de ondas.

### `ejercicio_2_transformada_discreta_fourier.py`

*   **Descripción:** Implementa la Transformada Discreta de Fourier (DFT) desde cero para una señal simple. Se explica cómo se calcula la magnitud y la fase de las componentes de frecuencia.
*   **Conceptos Clave:** DFT, componentes de frecuencia, magnitud, fase, espectro de frecuencia.

### `ejercicio_3_transformada_rapida_fourier_fft.py`

*   **Descripción:** Demuestra el uso de la Transformada Rápida de Fourier (FFT) de NumPy (`np.fft.fft`) para analizar señales. Se compara la eficiencia y la facilidad de uso con la implementación manual de la DFT. Se aplica a una señal con ruido.
*   **Conceptos Clave:** FFT, `np.fft.fft`, `np.fft.fftfreq`, `np.fft.fftshift`, análisis de ruido, filtrado conceptual.

### `ejercicio_4_aplicacion_analisis_vibraciones.py`

*   **Descripción:** Aplica la FFT para analizar datos de vibración de un sistema mecánico. Se identifican las frecuencias dominantes en la señal, lo cual es crucial para el diagnóstico de fallas en maquinaria o el análisis de resonancia.
*   **Conceptos Clave:** Análisis de vibraciones, diagnóstico de fallas, frecuencias dominantes, resonancia, datos experimentales.
