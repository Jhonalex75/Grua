import pandas as pd
import numpy as np
import os
import warnings
from datetime import datetime

# 1. CONFIGURACIÓN INICIAL
def configuracion_inicial():
    ruta_base = r'C:\Users\User\OneDrive\Documents\EL GRAN PORVENIR\PLAN OPEX'
    archivo_origen = 'SALIDA_2024_2025.xlsx'
    
    if not os.path.exists(ruta_base):
        raise FileNotFoundError(f"Directorio no encontrado: {ruta_base}")
    
    ruta_completa = os.path.join(ruta_base, archivo_origen)
    
    print(f"\n{'='*50}")
    print(f"Inicio de proceso: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if not os.path.exists(ruta_completa):
        print("Archivos disponibles:")
        print(os.listdir(ruta_base))
        raise FileNotFoundError(f"Archivo {archivo_origen} no encontrado")
    
    return ruta_base, ruta_completa

# 2. CARGA DE DATOS
def cargar_datos(ruta):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df = pd.read_excel(ruta, sheet_name=None, engine='openpyxl')
            return pd.concat(df.values(), ignore_index=True)
    except Exception as e:
        raise RuntimeError(f"Error al cargar datos: {str(e)}")

# 3. PROCESAMIENTO DE DATOS
def procesar_datos(df):
    # Filtrar años relevantes y datos esenciales
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce', dayfirst=True)
    df = df.dropna(subset=['Fecha', 'Costo Operación'])
    df = df[(df['Fecha'].dt.year >= 2024) & (df['Fecha'].dt.year <= 2025)]
    
    if df.empty:
        raise ValueError("No hay datos válidos para 2024-2025")
    
    # Calcular estadísticas mensuales
    df['Mes'] = df['Fecha'].dt.month
    stats = df.groupby(['Descripción del Producto', 'Mes']).agg(
        media=('Costo Operación', 'mean'),
        desviacion=('Costo Operación', 'std')
    ).reset_index()
    
    return stats

# 4. SIMULACIÓN MONTHLY MONTECARLO
def simular_proyeccion(stats):
    np.random.seed(42)
    proyecciones = []
    
    productos = stats['Descripción del Producto'].unique()
    
    for producto in productos:
        datos_producto = stats[stats['Descripción del Producto'] == producto]
        
        for mes in range(1, 13):
            # Obtener parámetros del mes
            mask = datos_producto['Mes'] == mes
            if mask.any():
                media = datos_producto.loc[mask, 'media'].values[0]
                desviacion = datos_producto.loc[mask, 'desviacion'].values[0]
            else:
                # Si no hay datos históricos para el mes
                media = datos_producto['media'].mean()
                desviacion = media * 0.2
            
            # Asegurar desviación mínima
            desviacion = max(desviacion, media * 0.1)
            
            # Generar simulación
            simulacion = np.random.normal(media, desviacion, 1)[0]
            proyecciones.append({
                'Descripción': producto,
                'Mes': mes,
                'Costo_Proyectado': max(round(simulacion, 2), 0)
            })
    
    return pd.DataFrame(proyecciones)

# 5. EXPORTACIÓN
def exportar_resultados(df, ruta_base):
    pivot = df.pivot_table(
        index='Descripción',
        columns='Mes',
        values='Costo_Proyectado',
        aggfunc='sum'
    ).reset_index().rename_axis(None, axis=1)
    
    pivot.columns = [
        'Descripción', 'Enero', 'Febrero', 'Marzo', 'Abril',
        'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre',
        'Octubre', 'Noviembre', 'Diciembre'
    ]
    
    archivo_destino = os.path.join(ruta_base, 'Proyeccion_Mensual_2026.xlsx')
    pivot.to_excel(archivo_destino, index=False)
    print(f"\nArchivo generado: {archivo_destino}")

# EJECUCIÓN
if __name__ == "__main__":
    try:
        ruta_base, ruta_archivo = configuracion_inicial()
        datos = cargar_datos(ruta_archivo)
        stats = procesar_datos(datos)
        proyecciones = simular_proyeccion(stats)
        exportar_resultados(proyecciones, ruta_base)
        print("\n¡Proceso completado exitosamente!")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        print("Verifique que:")
        print("- El archivo tenga datos entre 2024-2025")
        print("- Las columnas 'Fecha' y 'Costo Operación' sean válidas")
        print("- Los formatos de fecha sean reconocibles (ej: 15/01/2024)")