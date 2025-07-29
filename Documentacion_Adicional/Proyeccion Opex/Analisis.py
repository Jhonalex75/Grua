import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xlsxwriter

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

# Calcular frecuencia de consumo por mes
frecuencia_consumo = df.iloc[:, 5:].apply(lambda x: (x > 0).sum(), axis=0)

# Identificar los repuestos mayormente consumidos
df["Total Consumo"] = df.iloc[:, 5:].sum(axis=1)
repuestos_mas_consumidos = df.nlargest(5, "Total Consumo")["Descripción del Producto"]

# Definir la ruta para el nuevo archivo
output_path = r'C:\Users\User\OneDrive\Documents\EL GRAN PORVENIR\PLAN OPEX\Analisis_Consumo_Repuestos.xlsx'

# Crear archivo Excel con xlsxwriter
with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
    workbook = writer.book
    worksheet = workbook.add_worksheet('Análisis')
    
    # Definir formatos
    title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center', 'border': 1})
    header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
    number_format = workbook.add_format({'num_format': '$#,##0', 'border': 1})

    # Escribir título
    worksheet.merge_range('A1:D1', 'Análisis de Consumo de Repuestos', title_format)
    
    # Escribir estadísticas de consumo
    worksheet.write('A3', 'Estadísticas de Consumo Mensual', header_format)
    for i, (index, value) in enumerate(estadisticas_consumo.items(), start=4):
        worksheet.write(f'A{i}', index)
        worksheet.write(f'B{i}', value, number_format)
    
    # Escribir productos más costosos
    worksheet.write('A7', 'Top 10 Repuestos más Costosos', header_format)
    worksheet.write('A8', 'Descripción del Producto', header_format)
    worksheet.write('B8', 'Costo Total', header_format)
    for i, row in enumerate(productos_mas_costosos.itertuples(), start=9):
        worksheet.write(f'A{i}', row[1])
        worksheet.write(f'B{i}', row[2], number_format)
    
    # Crear gráfico de frecuencia de consumo por mes con los repuestos más consumidos
    plt.figure(figsize=(12, 6))
    colores = sns.color_palette("husl", len(repuestos_mas_consumidos))
    for i, repuesto in enumerate(repuestos_mas_consumidos):
        repuesto_data = df[df["Descripción del Producto"] == repuesto].iloc[:, 5:].sum()
        plt.plot(repuesto_data.index, repuesto_data.values, marker='o', linestyle='-', label=repuesto, color=colores[i])
    
    plt.title("Frecuencia de Consumo de Repuestos por Mes")
    plt.xlabel("Mes")
    plt.ylabel("Cantidad de Repuestos Consumidos")
    plt.xticks(rotation=45)
    plt.legend(title="Repuestos Más Consumidos")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('frecuencia_consumo.png', dpi=300, bbox_inches='tight')
    plt.close()
    worksheet.insert_image('D35', 'frecuencia_consumo.png')
    
    # Guardar y cerrar archivo
    print(f"Archivo de análisis creado exitosamente: {output_path}")
