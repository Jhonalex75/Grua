import numpy as np
import matplotlib.pyplot as plt

# Parámetros para cada región de la curva de la bañera
alpha1, beta1 = 1000, 0.5  # Mortalidad infantil (fallos decrecientes)
alpha2, beta2 = 1000, 1.0  # Vida útil (fallos constantes)
alpha3, beta3 = 1000, 3.0  # Desgaste (fallos crecientes)

# Tiempo
t = np.linspace(0.1, 3000, 1000)  # evitar t=0 para evitar división por cero

# Calcular tasas de fallo utilizando la fórmula de la función de riesgo
h_infantil = (beta1 / alpha1) * (t / alpha1) ** (beta1 - 1)
h_util = (beta2 / alpha2) * (t / alpha2) ** (beta2 - 1)
h_desgaste = (beta3 / alpha3) * (t / alpha3) ** (beta3 - 1)

# Inicializar arreglo de tasas
h_bathtub = np.zeros_like(t)

# Combinar por tramos
h_bathtub[t < 1000] = h_infantil[t < 1000]
h_bathtub[(t >= 1000) & (t < 2000)] = h_util[(t >= 1000) & (t < 2000)]
h_bathtub[t >= 2000] = h_desgaste[t >= 2000]

# Graficar
plt.figure(figsize=(10, 6))
plt.plot(t, h_bathtub, label="Curva de la Bañera", color="blue")
plt.title("Curva de la Bañera (Tasa de Fallos)")
plt.xlabel("Tiempo (horas)")
plt.ylabel("Tasa de Fallos")
plt.legend()
plt.grid(True)
plt.show()
