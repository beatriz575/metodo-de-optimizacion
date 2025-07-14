import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle

# Cargar datos desde tu archivo
df = pd.read_excel("C:/beatrizumiña/metodo-de-optimizacion/Tarea_15_Unit2/articulo_cientifico/dataset_limpio_final.xlsx")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df['puntaje_lectura'] = pd.to_numeric(df['puntaje_lectura'], errors='coerce')

# Agrupar por departamento y calcular promedio
departamento_mean = df.groupby("departamento")["puntaje_lectura"].mean().sort_values(ascending=False)
print("\n📊 Promedio de puntaje en lectura por departamento:")
print(departamento_mean)

# Convertir a DataFrame
df_heat = departamento_mean.reset_index()
df_heat.columns = ['departamento', 'puntaje_lectura']

def crear_heatmap_profesional(df_heat):
    """
    Crea un heat map profesional con diseño mejorado y ordenado
    """
    # Definir categorías de riesgo basadas en distribución de datos
    Q1 = df_heat['puntaje_lectura'].quantile(0.2)  # 20% más bajo
    Q2 = df_heat['puntaje_lectura'].quantile(0.4)  # 40%
    Q3 = df_heat['puntaje_lectura'].quantile(0.6)  # 60%
    Q4 = df_heat['puntaje_lectura'].quantile(0.8)  # 80%
    
    def categorizar_riesgo(puntaje):
        if puntaje <= Q1:
            return 'Crítico'
        elif puntaje <= Q2:
            return 'Alto'
        elif puntaje <= Q3:
            return 'Medio'
        elif puntaje <= Q4:
            return 'Bajo'
        else:
            return 'Óptimo'
    
    df_heat['categoria_riesgo'] = df_heat['puntaje_lectura'].apply(categorizar_riesgo)
    
    # Definir colores para cada categoría
    colores_categoria = {
        'Crítico': '#d73027',    # Rojo intenso
        'Alto': '#f46d43',       # Rojo-naranja
        'Medio': '#fee08b',      # Amarillo
        'Bajo': '#a6d96a',       # Verde claro
        'Óptimo': '#1a9850'      # Verde intenso
    }
    
    # Organizar departamentos por categorías
    categorias = ['Crítico', 'Alto', 'Medio', 'Bajo', 'Óptimo']
    max_por_categoria = max(len(df_heat[df_heat['categoria_riesgo'] == cat]) for cat in categorias)
    
    # Crear figura con diseño mejorado
    fig = plt.figure(figsize=(20, 12))
    
    # Crear layout con GridSpec para mejor control
    gs = fig.add_gridspec(3, 3, height_ratios=[0.1, 0.8, 0.1], width_ratios=[0.7, 0.02, 0.28])
    
    # Subplot principal para el heatmap
    ax_main = fig.add_subplot(gs[1, 0])
    
    # Crear matriz para el heatmap
    matriz_puntajes = np.full((len(categorias), max_por_categoria), np.nan)
    matriz_nombres = np.full((len(categorias), max_por_categoria), '', dtype=object)
    matriz_colores = np.full((len(categorias), max_por_categoria), np.nan)
    
    for i, categoria in enumerate(categorias):
        deps_categoria = df_heat[df_heat['categoria_riesgo'] == categoria].sort_values('puntaje_lectura', ascending=False)
        for j, (_, row) in enumerate(deps_categoria.iterrows()):
            if j < max_por_categoria:
                matriz_puntajes[i, j] = row['puntaje_lectura']
                matriz_nombres[i, j] = row['departamento']
                matriz_colores[i, j] = i + 1
    
    # Crear colormap personalizado
    colors = ['#d73027', '#f46d43', '#fee08b', '#a6d96a', '#1a9850']
    cmap = LinearSegmentedColormap.from_list('riesgo', colors, N=5)
    
    # Crear el heatmap base
    mask = np.isnan(matriz_puntajes)
    im = ax_main.imshow(matriz_colores, cmap=cmap, aspect='auto', vmin=1, vmax=5)
    
    # Agregar texto en cada celda con mejor formato
    for i in range(len(categorias)):
        for j in range(max_por_categoria):
            if not mask[i, j]:
                text_color = 'white' if i <= 1 else 'black'
                ax_main.text(j, i, f'{matriz_nombres[i, j]}\n{matriz_puntajes[i, j]:.0f}',
                           ha='center', va='center', 
                           fontsize=12, fontweight='bold',
                           color=text_color)
    
    # Configurar ejes del heatmap
    ax_main.set_xticks(range(max_por_categoria))
    ax_main.set_xticklabels([f'Dept. {i+1}' for i in range(max_por_categoria)], fontsize=11)
    ax_main.set_yticks(range(len(categorias)))
    ax_main.set_yticklabels(categorias, fontsize=14, fontweight='bold')
    
    # Agregar líneas de separación más elegantes
    for i in range(len(categorias) + 1):
        ax_main.axhline(i - 0.5, color='white', linewidth=3)
    for j in range(max_por_categoria + 1):
        ax_main.axvline(j - 0.5, color='white', linewidth=1.5)
    
    # Título principal
    fig.suptitle('Mapa de Calor: Categorización del Rendimiento Académico en Lectura por Departamento', 
                fontsize=20, fontweight='bold', y=0.95)
    ax_main.set_title('Evaluación Muestral 2022 - Ministerio de Educación del Perú', 
                     fontsize=14, style='italic', pad=20)
    
    # Panel derecho para leyenda y estadísticas
    ax_legend = fig.add_subplot(gs[1, 2])
    ax_legend.axis('off')
    
    # Crear leyenda de colores más ordenada
    legend_y = 0.85
    ax_legend.text(0.05, 0.95, 'NIVELES DE RIESGO EDUCATIVO', 
                  fontsize=14, fontweight='bold', transform=ax_legend.transAxes)
    
    for i, categoria in enumerate(categorias):
        color = colors[i]
        count = len(df_heat[df_heat['categoria_riesgo'] == categoria])
        
        # Dibujar rectángulo de color
        rect = Rectangle((0.05, legend_y - i*0.12), 0.08, 0.08, 
                        facecolor=color, edgecolor='black', linewidth=1,
                        transform=ax_legend.transAxes)
        ax_legend.add_patch(rect)
        
        # Agregar texto
        ax_legend.text(0.18, legend_y - i*0.12 + 0.04, 
                      f'{categoria}', 
                      fontsize=12, fontweight='bold', 
                      transform=ax_legend.transAxes, va='center')
        ax_legend.text(0.18, legend_y - i*0.12 - 0.02, 
                      f'({count} departamentos)', 
                      fontsize=10, style='italic', color='gray',
                      transform=ax_legend.transAxes, va='center')
    
    # Separador
    ax_legend.plot([0.05, 0.95], [0.25, 0.25], color='gray', linewidth=1,
                  transform=ax_legend.transAxes)
    
    # Estadísticas generales más ordenadas
    ax_legend.text(0.05, 0.20, 'ESTADÍSTICAS GENERALES', 
                  fontsize=14, fontweight='bold', transform=ax_legend.transAxes)
    
    # Datos de estadísticas
    puntaje_max = df_heat['puntaje_lectura'].max()
    puntaje_min = df_heat['puntaje_lectura'].min()
    dept_max = df_heat.loc[df_heat['puntaje_lectura'].idxmax(), 'departamento']
    dept_min = df_heat.loc[df_heat['puntaje_lectura'].idxmin(), 'departamento']
    brecha = puntaje_max - puntaje_min
    promedio = df_heat['puntaje_lectura'].mean()
    desv_std = df_heat['puntaje_lectura'].std()
    
    # Mostrar estadísticas de forma más organizada
    stats_info = [
        f"Puntaje más alto: {puntaje_max:.1f}",
        f"    ({dept_max})",
        f"Puntaje más bajo: {puntaje_min:.1f}",
        f"    ({dept_min})",
        f"Brecha educativa: {brecha:.1f} puntos",
        f"Promedio nacional: {promedio:.1f} puntos",
        f"Desviación estándar: {desv_std:.1f} puntos"
    ]
    
    # Posicionar cada línea individualmente
    y_start = 0.16
    for i, stat in enumerate(stats_info):
        y_pos = y_start - i*0.030
        if stat.startswith('    '):  # Líneas indentadas
            ax_legend.text(0.08, y_pos, stat, fontsize=9, style='italic', 
                          color='gray', transform=ax_legend.transAxes)
        else:  # Líneas principales
            ax_legend.text(0.05, y_pos, stat, fontsize=10, fontweight='bold',
                          transform=ax_legend.transAxes)
    
    # Ajustar layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.92, right=0.98, left=0.05, bottom=0.05)
    
    # Guardar con alta resolución
    plt.savefig('heatmap_rendimiento_academico.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.show()
    
    # Mostrar resumen por categorías en consola
    print("\n📊 Resumen detallado por categorías de riesgo:")
    print("="*70)
    for categoria in categorias:
        deps = df_heat[df_heat['categoria_riesgo'] == categoria]
        if len(deps) > 0:
            print(f"\n🔸 {categoria.upper()}:")
            print(f"   Departamentos: {', '.join(deps['departamento'].tolist())}")
            print(f"   Rango: {deps['puntaje_lectura'].min():.1f} - {deps['puntaje_lectura'].max():.1f}")
            print(f"   Promedio: {deps['puntaje_lectura'].mean():.1f}")
            print(f"   Cantidad: {len(deps)} departamentos")
            print(f"   Porcentaje: {(len(deps)/len(df_heat)*100):.1f}% del total")

# Ejecutar la función
if __name__ == "__main__":
    print("Generando Heat Map profesional mejorado...")
    crear_heatmap_profesional(df_heat)
    print("\n✅ Heat map generado exitosamente con diseño mejorado!")
    print("Archivo guardado: heatmap_rendimiento_academico.png")