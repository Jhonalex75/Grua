"""
INTRODUCCIÓN AL ANÁLISIS DE GRÚAS (EJEMPLO RÁPIDO)
==================================================

Este script simula un cálculo básico de momento de vuelco para una grúa móvil,
demostrando los conceptos físicos fundamentales del curso.

Conceptos:
    - Momento de Carga = Peso Carga * Radio
    - Momento de Contrapeso = Peso Grúa * Distancia CG
    - Factor de Estabilidad = Momento Estabilizador / Momento Volcador

Autor: Jhonalex75
"""

import matplotlib.pyplot as plt
import numpy as np

def analizar_estabilidad_basica(peso_carga_ton, radio_m, capacidad_max_ton):
    print(f"--- ANÁLISIS DE IZAJE: Carga {peso_carga_ton} ton @ {radio_m} m ---")
    
    # 1. Cálculo de Capacidad Nominal (Simplificado)
    # Supongamos una curva de carga inversa: Capacidad ~ K / Radio
    k_grua = capacidad_max_ton * 3 # Constante de la grúa (ton*m)
    capacidad_al_radio = k_grua / radio_m
    
    print(f"Capacidad de tabla al radio {radio_m}m: {capacidad_al_radio:.2f} ton")
    
    # 2. Porcentaje de Capacidad
    porcentaje = (peso_carga_ton / capacidad_al_radio) * 100
    print(f"Uso de capacidad: {porcentaje:.1f}%")
    
    # 3. Evaluación
    if porcentaje > 100:
        estado = "CRÍTICO - NO SEGURO"
        color = 'red'
    elif porcentaje > 85:
        estado = "ALERTA - IZAJE CRÍTICO"
        color = 'orange'
    else:
        estado = "SEGURO"
        color = 'green'
        
    print(f"Estado del Izaje: {estado}")
    return porcentaje, estado, color

def visualizar_semaforo(porcentaje, estado, color):
    fig, ax = plt.subplots(figsize=(6, 2))
    
    # Barra de progreso
    ax.barh([0], [100], color='lightgray', height=0.5)
    ax.barh([0], [min(porcentaje, 100)], color=color, height=0.5)
    
    # Líneas límite
    ax.axvline(x=85, color='orange', linestyle='--', label='Límite Crítico (85%)')
    ax.axvline(x=100, color='red', linestyle='-', label='Capacidad Máxima (100%)')
    
    ax.set_xlim(0, 110)
    ax.set_yticks([])
    ax.set_xlabel('Porcentaje de Capacidad (%)')
    ax.set_title(f'Estado: {estado} ({porcentaje:.1f}%)')
    ax.legend(loc='upper right', fontsize='small')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Prueba del script
    carga = 12   # toneladas
    radio = 15   # metros
    cap_max = 80 # toneladas (capacidad máxima absoluta de la grúa)
    
    pct, est, col = analizar_estabilidad_basica(carga, radio, cap_max)
    visualizar_semaforo(pct, est, col)
