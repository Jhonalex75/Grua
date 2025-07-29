import pandas as pd
import numpy as np

# Ruta del archivo
file_path = r"C:\Users\User\OneDrive\Documents\EL GRAN PORVENIR\PLAN OPEX\SALIDA MATERIAL.xlsx"
sheet_name = "SALIDA MATERIAL"  # Asegúrate de que este sea el nombre correcto de la hoja

# Leer el archivo Excel
try:
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    print("Datos cargados correctamente:")
    print(df.head())  # Mostrar las primeras filas del DataFrame

except FileNotFoundError:
    print(f"Error: No se encontró el archivo en la ruta especificada: {file_path}")
    exit()
except ValueError as e:
    print(f"Error al leer la hoja de cálculo: {e}")
    exit()
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
    exit()

# Asegurarse de que las columnas sean tratadas como texto y eliminar espacios adicionales
df['Cliente'] = df['Cliente'].astype(str).str.strip()
df['Costo Operación'] = pd.to_numeric(df['Costo Operación'], errors='coerce')  # Convertir a numérico

# Filtrar por "MANTENIMIENTO MECANICO" en la columna 'Cliente'
mantenimiento_mecanico = df[df['Cliente'].str.contains("MANTENIMIENTO MECANICO", na=False, case=False)]

# Verificar si hay datos filtrados
if mantenimiento_mecanico.empty:
    print("No se encontraron datos relacionados con 'MANTENIMIENTO MECANICO' en la columna 'Cliente'.")
    exit()
else:
    print("Datos filtrados correctamente:")
    print(mantenimiento_mecanico.head())

# Crear un nuevo DataFrame para la proyección
proyeccion = pd.DataFrame(columns=["Descripción del Producto", "Cantidad", "Valor Unitario", "Costo Operación"] + 
                            [f"{month} 2025" for month in ["Enero", "Febrero", "Marzo", "Abril", 
                                                              "Mayo", "Junio", "Julio", "Agosto", 
                                                              "Septiembre", "Octubre", "Noviembre", 
                                                              "Diciembre"]])

# Método Montecarlo para proyecciones (ejemplo simple)
def montecarlo_projection(row, simulations=1000):
    consumo_historial = []
    for _ in range(simulations):
        # Simular un consumo aleatorio basado en el historial
        simulated_consumo = np.random.normal(loc=row['Salidas'], scale=row['Salidas'] * 0.1)  # 10% de variación
        consumo_historial.append(simulated_consumo)
    
    return np.mean(consumo_historial)

# Iterar sobre cada producto filtrado y proyectar consumos y costos
for index, row in mantenimiento_mecanico.iterrows():
    descripcion = row['Descripción del Producto']  # Cambiado a 'Descripción del Producto'
    cantidad = row['Salidas']
    valor_unitario = row['Costo Unitario']
    costo_operacion = row['Costo Operación']
    
    # Proyección usando Montecarlo
    projected_consumo = montecarlo_projection(row)
    
    # Agregar al DataFrame de proyección
    proyeccion = proyeccion.append({
        "Descripción del Producto": descripcion,
        "Cantidad": projected_consumo,
        "Valor Unitario": valor_unitario,
        "Costo Operación": costo_operacion,  # Mantener el costo de operación original
        **{f"{month} 2025": projected_consumo * valor_unitario for month in ["Enero", "Febrero", 
                                                                             "Marzo", "Abril", 
                                                                             "Mayo", "Junio", 
                                                                             "Julio", "Agosto", 
                                                                             "Septiembre", "Octubre", 
                                                                             "Noviembre", "Diciembre"]}
    }, ignore_index=True)

# Agregar todos los ítems de 'Descripción del Producto' a la nueva hoja desde la segunda fila
for index, row in df.iterrows():
    if row['Descripción del Producto'] not in proyeccion["Descripción del Producto"].values:
        proyeccion = proyeccion.append({
            "Descripción del Producto": row["Descripción del Producto"],
            "Cantidad": None,  # O puedes poner un valor por defecto
            "Valor Unitario": None,  # O puedes poner un valor por defecto
            "Costo Operación": None,  # O puedes poner un valor por defecto
            **{f"{month} 2025": None for month in ["Enero", "Febrero",
                                                     "Marzo", "Abril",
                                                     "Mayo", "Junio",
                                                     "Julio", "Agosto",
                                                     "Septiembre", "Octubre",
                                                     "Noviembre", "Diciembre"]}
        }, ignore_index=True)

# Verificar si el DataFrame 'proyeccion' tiene datos antes de guardarlo
if proyeccion.empty:
    print("El DataFrame 'proyeccion' está vacío. No se generaron datos para guardar.")
    exit()
else:
    print("Datos generados para la proyección:")
    print(proyeccion.head())

# Definir la ruta de salida para el nuevo archivo
output_path = r"C:\Users\User\OneDrive\Documents\EL GRAN PORVENIR\PLAN OPEX\Proyeccion_Opex_2025.xlsx"

# Guardar en un nuevo archivo Excel
try:
    # Crear un ExcelWriter object
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        # Guardar el DataFrame en una hoja llamada 'Proyección 2025'
        proyeccion.to_excel(writer, sheet_name='Proyección 2025', index=False)
        
        # Obtener el workbook y la hoja
        workbook = writer.book
        worksheet = writer.sheets['Proyección 2025']
        
        # Ajustar el ancho de las columnas automáticamente
        for idx, col in enumerate(proyeccion.columns):
            column_width = max(proyeccion[col].astype(str).apply(len).max(), len(col)) + 2
            worksheet.set_column(idx, idx, column_width)
    
    print(f"\nArchivo guardado exitosamente en: {output_path}")

except PermissionError:
    print("Error: No se pudo guardar el archivo. Asegúrate de que el archivo no esté abierto en Excel.")
except Exception as e:
    print(f"Error al guardar el archivo: {e}")

