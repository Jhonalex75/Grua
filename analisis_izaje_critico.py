"""
ANÁLISIS DE IZAJE CRÍTICO Y ESTABILIDAD DE GRÚA
=================================================

Este script modela la estabilidad de una grúa móvil y determina si una operación
de izaje es segura (Zona Verde) o crítica/insegura (Zona Roja).

Principios de Ingeniería:
    1. Equilibrio de Momentos: M_estabilizador >= M_vuelco * Factor_Seguridad
    2. Curva de Capacidad: La carga máxima disminuye a medida que aumenta el radio.

Variables:
    - Radio (R): Distancia horizontal desde el centro de rotación [m]
    - Carga (W): Peso del objeto a izar [kg]
    - Contrapeso: Masa trasera para estabilidad [kg]
"""

import numpy as np
import matplotlib.pyplot as plt

class GruaMovil:
    def __init__(self, capacidad_max_ton, longitud_pluma_max):
        self.cap_max = capacidad_max_ton * 1000 # kg
        self.l_max = longitud_pluma_max # m
        
        # Modelo simplificado de curva de carga (Hiperbola aproximada: Carga * Radio = Constante)
        # Constante K ajustada para que a radio mínimo (ej. 3m) de la capacidad máxima
        self.radio_min = 3.0
        self.K = self.cap_max * self.radio_min 

    def capacidad_al_radio(self, radio):
        """Calcula la capacidad bruta de la grúa a un radio dado."""
        if radio < self.radio_min:
            return self.cap_max
        
        # Modelo simplificado: Capacidad decae con el radio
        cap = self.K / radio
        
        # Limitación física por longitud de pluma (simplificado)
        if radio > self.l_max * 0.85: # Ángulo muy bajo
            cap = 0
            
        return cap

    def evaluar_izaje(self, radio_izaje, carga_izaje):
        """
        Evalúa si un izaje es seguro.
        Retorna: (Factor de Uso %, Estado)
        """
        cap_limite = self.capacidad_al_radio(radio_izaje)
        
        if cap_limite <= 0:
            return 999.0, "FUERA DE RANGO"
            
        uso = (carga_izaje / cap_limite) * 100
        
        if uso > 100:
            estado = "CRÍTICO - VUELCO INMINENTE"
        elif uso > 75:
            estado = "ALERTA - IZAJE CRÍTICO (>75%)"
        else:
            estado = "SEGURO"
            
        return uso, estado, cap_limite

def graficar_semaforo_estabilidad(grua, radio_op, carga_op):
    """Genera el gráfico de semáforo de estabilidad."""
    radios = np.linspace(grua.radio_min, grua.l_max * 0.9, 100)
    capacidades = [grua.capacidad_al_radio(r) / 1000 for r in radios] # en Toneladas
    
    plt.figure(figsize=(10, 6))
    
    # 1. Zona Segura (Verde)
    plt.fill_between(radios, 0, [c * 0.75 for c in capacidades], color='green', alpha=0.3, label='Zona Segura (<75%)')
    
    # 2. Zona Crítica (Amarillo)
    plt.fill_between(radios, [c * 0.75 for c in capacidades], capacidades, color='yellow', alpha=0.3, label='Zona Crítica (75-100%)')
    
    # 3. Zona de Falla (Rojo)
    plt.fill_between(radios, capacidades, max(capacidades)*1.1, color='red', alpha=0.3, label='Zona de Vuelco (>100%)')
    
    # 4. Curva Límite
    plt.plot(radios, capacidades, 'k-', linewidth=2, label='Límite de Capacidad')
    
    # 5. Punto de Operación
    carga_ton = carga_op / 1000
    uso, estado, cap_lim = grua.evaluar_izaje(radio_op, carga_op)
    
    color_punto = 'black'
    if uso > 100: color_punto = 'red'
    elif uso > 75: color_punto = 'orange'
    else: color_punto = 'green'
    
    plt.scatter(radio_op, carga_ton, color=color_punto, s=150, edgecolors='black', zorder=10, label='Punto de Izaje')
    
    # Anotaciones
    plt.title(f"Análisis de Estabilidad - Estado: {estado}", fontsize=14, fontweight='bold')
    plt.xlabel("Radio de Trabajo [m]", fontsize=12)
    plt.ylabel("Carga [Toneladas]", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    
    # Caja de texto con detalles
    info = (
        f"Radio: {radio_op} m\n"
        f"Carga: {carga_ton} Ton\n"
        f"Capacidad: {cap_lim/1000:.2f} Ton\n"
        f"% Uso: {uso:.1f}%"
    )
    plt.text(0.7, 0.8, info, transform=plt.gca().transAxes, 
             bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray'))
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # --- SIMULACIÓN DE IZAJE ---
    # Grúa de 50 Toneladas, Pluma de 30 metros
    mi_grua = GruaMovil(capacidad_max_ton=50, longitud_pluma_max=30)
    
    # Caso de Prueba: Izaje de un generador de 12 Toneladas a 8 metros
    radio_operacion = 8.0 # metros
    carga_operacion = 12000 # kg
    
    print("--- REPORTE DE IZAJE ---")
    uso, estado, limite = mi_grua.evaluar_izaje(radio_operacion, carga_operacion)
    print(f"Estado: {estado}")
    print(f"Capacidad al radio {radio_operacion}m: {limite:.2f} kg")
    print(f"Carga Actual: {carga_operacion} kg")
    print(f"Porcentaje de Uso: {uso:.2f}%")
    
    graficar_semaforo_estabilidad(mi_grua, radio_operacion, carga_operacion)
