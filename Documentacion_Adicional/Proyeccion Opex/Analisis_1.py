import pandas as pd
import matplotlib.pyplot as plt

# Ruta del archivo de Excel
file_path = r'C:\Users\User\OneDrive\Documents\EL GRAN PORVENIR\PLAN OPEX\Proyeccion_Opex_2025_REV_1.xlsx'

# Cargar datos
xls = pd.ExcelFile(file_path)
df = pd.read_excel(xls, sheet_name="Proyección 2025")   
# Calcular consumo total por mes
consumo_mensual = df.iloc[:, 5:].sum()


# Calcular estadísticas descriptivas
estadisticas_consumo = consumo_mensual.describe()

# Identificar el mes con mayor y menor consumo
mes_mayor_consumo = consumo_mensual.idxmax()
mes_menor_consumo = consumo_mensual.idxmin()

# Identificar los productos más costosos
df["Costo Total"] = df["Costo Operación"]
productos_mas_costosos = df.nlargest(10, "Costo Total")[["Descripción del Producto", "Costo Total"]]

# Guardar resultados en un archivo Excel
output_path = r'C:\Users\User\OneDrive\Documents\EL GRAN PORVENIR\PLAN OPEX\Analisis_Consumo_Repuestos.xlsx'
with pd.ExcelWriter(output_path) as writer:
    consumo_mensual.to_frame(name="Consumo Mensual").to_excel(writer, sheet_name="Consumo Mensual")
    productos_mas_costosos.to_excel(writer, sheet_name="Top Productos Costosos")
    estadisticas_consumo.to_frame(name="Estadísticas").to_excel(writer, sheet_name="Estadísticas")

# Graficar tendencias de consumo
plt.figure(figsize=(12, 6))
plt.plot(consumo_mensual.index, consumo_mensual.values, marker='o', linestyle='-')
plt.title("Tendencia de Consumo de Repuestos en 2025")
plt.xlabel("Mes")
plt.ylabel("Costo Total de Repuestos")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Crear gráfico de barras para los productos más costosos
plt.figure(figsize=(15, 8))
bars = plt.bar(productos_mas_costosos['Descripción del Producto'], 
               productos_mas_costosos['Costo Total'])

# Personalizar el gráfico
plt.title('Top 10 Repuestos más Costosos', fontsize=14, pad=20)
plt.xlabel('Descripción del Producto', fontsize=12)
plt.ylabel('Costo Total', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# Añadir etiquetas de valor sobre cada barra
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'${height:,.0f}',
             ha='center', va='bottom')

# Ajustar el diseño para evitar que se corten las etiquetas
plt.tight_layout()
plt.show()

# Imprimir resultados
print("Mes con mayor consumo:", mes_mayor_consumo)
print("Mes con menor consumo:", mes_menor_consumo)
print("Estadísticas del consumo mensual:")
print(estadisticas_consumo)
