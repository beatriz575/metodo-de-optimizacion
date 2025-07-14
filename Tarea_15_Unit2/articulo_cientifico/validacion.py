import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo de gráficas
plt.style.use('default')
sns.set_palette("husl")

# Resultados reales obtenidos
resultados_reales = {
    'lectura': {
        'pso': {'mse_mean': 4871.77, 'r2_mean': 0.2026, 'params': {'n_estimators': 88, 'max_depth': 6}},
        'optuna': {'mse_mean': 4872.12, 'r2_mean': 0.2025, 'params': {'n_estimators': 177, 'max_depth': 6}}
    },
    'matematica': {
        'pso': {'mse_mean': 6650.12, 'r2_mean': 0.1538, 'params': {'n_estimators': 180, 'max_depth': 7}},
        'optuna': {'mse_mean': 6650.51, 'r2_mean': 0.1538, 'params': {'n_estimators': 152, 'max_depth': 7}}
    }
}

def cargar_y_preparar_datos():
    """Carga y prepara el dataset"""
    df = pd.read_excel("C:/beatrizumiña/metodo-de-optimizacion/Tarea_15_Unit2/articulo_cientifico/dataset_limpio_final.xlsx")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    
    # Limpiar datos
    df['puntaje_lectura'] = pd.to_numeric(df['puntaje_lectura'], errors='coerce')
    df['puntaje_matematica'] = pd.to_numeric(df['puntaje_matematica'], errors='coerce')
    df = df.dropna(subset=['puntaje_lectura', 'puntaje_matematica'])
    
    return df

def grafica_1_distribucion_puntajes(df):
    """Gráfica 1: Distribución de puntajes en lectura y matemática"""
    plt.figure(figsize=(12, 6))
    
    # Subplot 1: Histogramas
    plt.subplot(1, 2, 1)
    plt.hist(df['puntaje_lectura'], bins=30, alpha=0.7, label='Lectura', color='skyblue', density=True)
    plt.hist(df['puntaje_matematica'], bins=30, alpha=0.7, label='Matemática', color='lightcoral', density=True)
    plt.xlabel('Puntaje')
    plt.ylabel('Densidad')
    plt.title('Distribución de Puntajes')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Subplot 2: Box plots
    plt.subplot(1, 2, 2)
    data_melted = df.melt(value_vars=['puntaje_lectura', 'puntaje_matematica'], 
                         var_name='Materia', value_name='Puntaje')
    data_melted['Materia'] = data_melted['Materia'].map({'puntaje_lectura': 'Lectura', 'puntaje_matematica': 'Matemática'})
    
    sns.boxplot(data=data_melted, x='Materia', y='Puntaje', palette=['skyblue', 'lightcoral'])
    plt.title('Distribución por Materia')
    plt.ylabel('Puntaje')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('grafica1_distribucion.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Gráfica 1 guardada: grafica1_distribucion.png")

def grafica_2_sexo(df):
    """Gráfica 2: Comparación por sexo"""
    plt.figure(figsize=(10, 6))
    
    try:
        # Verificar valores únicos de sexo
        print(f"Valores únicos en sexo: {df['sexo'].unique()}")
        
        # Mapear según los valores reales
        if df['sexo'].dtype == 'object':
            # Si ya son strings
            sexo_mapping = {'Hombre': 'Hombre', 'Mujer': 'Mujer', 'hombre': 'Hombre', 'mujer': 'Mujer'}
        else:
            # Si son números, mapear
            sexo_mapping = {0: 'Hombre', 1: 'Mujer', 'Hombre': 'Hombre', 'Mujer': 'Mujer'}
        
        # Preparar datos
        df_temp = df.copy()
        df_temp['sexo_label'] = df_temp['sexo'].map(sexo_mapping).fillna(df_temp['sexo'])
        
        # Crear gráfica manual con matplotlib
        sexos = df_temp['sexo_label'].unique()
        materias = ['puntaje_lectura', 'puntaje_matematica']
        materia_labels = ['Lectura', 'Matemática']
        colors = ['skyblue', 'lightcoral']
        
        positions = []
        data_to_plot = []
        labels = []
        colors_list = []
        
        pos = 0
        for i, sexo in enumerate(sexos):
            for j, (materia, label) in enumerate(zip(materias, materia_labels)):
                data = df_temp[df_temp['sexo_label'] == sexo][materia].dropna()
                data_to_plot.append(data)
                positions.append(pos)
                labels.append(f'{sexo}\n{label}')
                colors_list.append(colors[j])
                pos += 1
            pos += 0.5  # Espacio entre grupos
        
        # Crear boxplot
        bp = plt.boxplot(data_to_plot, positions=positions, patch_artist=True, widths=0.4)
        
        # Colorear
        for patch, color in zip(bp['boxes'], colors_list):
            patch.set_facecolor(color)
            patch.set_alpha(0.8)
        
        plt.xticks(positions, labels, rotation=0)
        plt.title('Comparación de Puntajes por Sexo', fontsize=14, fontweight='bold')
        plt.xlabel('Sexo y Materia')
        plt.ylabel('Puntaje')
        plt.grid(True, alpha=0.3, axis='y')
        
        # Leyenda manual
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor='skyblue', label='Lectura'),
                          Patch(facecolor='lightcoral', label='Matemática')]
        plt.legend(handles=legend_elements, title='Materia')
        
    except Exception as e:
        print(f"Error en gráfica de sexo: {e}")
        # Gráfica alternativa simple
        plt.subplot(1, 2, 1)
        df.boxplot(column='puntaje_lectura', by='sexo', ax=plt.gca())
        plt.title('Lectura por Sexo')
        plt.subplot(1, 2, 2)
        df.boxplot(column='puntaje_matematica', by='sexo', ax=plt.gca())
        plt.title('Matemática por Sexo')
    
    plt.tight_layout()
    plt.savefig('grafica2_sexo.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Gráfica 2 guardada: grafica2_sexo.png")

def grafica_3_zona(df):
    """Gráfica 3: Puntajes por zona geográfica"""
    plt.figure(figsize=(10, 6))
    
    try:
        # Verificar valores únicos de zona
        print(f"Valores únicos en zona: {df['zona'].unique()}")
        
        # Mapear según los valores reales
        if df['zona'].dtype == 'object':
            # Si ya son strings
            zona_mapping = {'Rural': 'Rural', 'Urbana': 'Urbana', 'rural': 'Rural', 'urbana': 'Urbana'}
        else:
            # Si son números, mapear
            zona_mapping = {0: 'Rural', 1: 'Urbana', 'Rural': 'Rural', 'Urbana': 'Urbana'}
        
        # Preparar datos
        df_temp = df.copy()
        df_temp['zona_label'] = df_temp['zona'].map(zona_mapping).fillna(df_temp['zona'])
        
        # Crear gráfica manual
        zonas = df_temp['zona_label'].unique()
        materias = ['puntaje_lectura', 'puntaje_matematica']
        materia_labels = ['Lectura', 'Matemática']
        colors = ['lightgreen', 'orange']
        
        positions = []
        data_to_plot = []
        labels = []
        colors_list = []
        
        pos = 0
        for i, zona in enumerate(zonas):
            for j, (materia, label) in enumerate(zip(materias, materia_labels)):
                data = df_temp[df_temp['zona_label'] == zona][materia].dropna()
                data_to_plot.append(data)
                positions.append(pos)
                labels.append(f'{zona}\n{label}')
                colors_list.append(colors[j])
                pos += 1
            pos += 0.5
        
        # Crear boxplot
        bp = plt.boxplot(data_to_plot, positions=positions, patch_artist=True, widths=0.4)
        
        # Colorear
        for patch, color in zip(bp['boxes'], colors_list):
            patch.set_facecolor(color)
            patch.set_alpha(0.8)
        
        plt.xticks(positions, labels, rotation=0)
        plt.title('Puntajes por Zona Geográfica', fontsize=14, fontweight='bold')
        plt.xlabel('Zona y Materia')
        plt.ylabel('Puntaje')
        plt.grid(True, alpha=0.3, axis='y')
        
        # Leyenda
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor='lightgreen', label='Lectura'),
                          Patch(facecolor='orange', label='Matemática')]
        plt.legend(handles=legend_elements, title='Materia')
        
    except Exception as e:
        print(f"Error en gráfica de zona: {e}")
        # Gráfica alternativa
        plt.subplot(1, 2, 1)
        df.boxplot(column='puntaje_lectura', by='zona', ax=plt.gca())
        plt.title('Lectura por Zona')
        plt.subplot(1, 2, 2)
        df.boxplot(column='puntaje_matematica', by='zona', ax=plt.gca())
        plt.title('Matemática por Zona')
    
    plt.tight_layout()
    plt.savefig('grafica3_zona.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Gráfica 3 guardada: grafica3_zona.png")

def grafica_4_nivel_socioeconomico(df):
    """Gráfica 4: Promedio de puntajes por nivel socioeconómico"""
    plt.figure(figsize=(12, 6))
    
    try:
        # Verificar valores únicos de NSE
        print(f"Valores únicos en nivel_socioeconomico: {df['nivel_socioeconomico'].unique()}")
        
        # Mapear niveles socioeconómicos
        if df['nivel_socioeconomico'].dtype == 'object':
            # Si ya son strings
            nse_mapping = {
                'Muy bajo': 'Muy bajo', 'Bajo': 'Bajo', 'Medio': 'Medio', 'Alto': 'Alto',
                'muy bajo': 'Muy bajo', 'bajo': 'Bajo', 'medio': 'Medio', 'alto': 'Alto'
            }
        else:
            # Si son números, mapear
            nse_mapping = {0: 'Muy bajo', 1: 'Bajo', 2: 'Medio', 3: 'Alto'}
        
        df_temp = df.copy()
        df_temp['nse_label'] = df_temp['nivel_socioeconomico'].map(nse_mapping).fillna(df_temp['nivel_socioeconomico'])
        
        # Calcular promedios
        promedios = df_temp.groupby('nse_label')[['puntaje_lectura', 'puntaje_matematica']].mean().reset_index()
        
        # Ordenar por orden lógico
        orden_deseado = ['Muy bajo', 'Bajo', 'Medio', 'Alto']
        promedios['orden'] = promedios['nse_label'].map({nivel: i for i, nivel in enumerate(orden_deseado)})
        promedios = promedios.sort_values('orden').reset_index(drop=True)
        
        # Gráfica de barras
        x = np.arange(len(promedios))
        width = 0.35
        
        bars1 = plt.bar(x - width/2, promedios['puntaje_lectura'], width, 
                       label='Lectura', color='skyblue', alpha=0.8)
        bars2 = plt.bar(x + width/2, promedios['puntaje_matematica'], width, 
                       label='Matemática', color='lightcoral', alpha=0.8)
        
        plt.xlabel('Nivel Socioeconómico')
        plt.ylabel('Puntaje Promedio')
        plt.title('Promedio de Puntajes por Nivel Socioeconómico', fontsize=14, fontweight='bold')
        plt.xticks(x, promedios['nse_label'])
        plt.legend()
        plt.grid(True, alpha=0.3, axis='y')
        
        # Añadir valores en las barras
        for i, (lec, mat) in enumerate(zip(promedios['puntaje_lectura'], promedios['puntaje_matematica'])):
            plt.text(i - width/2, lec + 5, f'{lec:.0f}', ha='center', va='bottom', fontweight='bold')
            plt.text(i + width/2, mat + 5, f'{mat:.0f}', ha='center', va='bottom', fontweight='bold')
            
    except Exception as e:
        print(f"Error en gráfica NSE: {e}")
        # Gráfica alternativa
        try:
            # Usar los datos tal como están
            promedios_alt = df.groupby('nivel_socioeconomico')[['puntaje_lectura', 'puntaje_matematica']].mean()
            
            x_alt = np.arange(len(promedios_alt))
            width = 0.35
            
            plt.bar(x_alt - width/2, promedios_alt['puntaje_lectura'], width, 
                   label='Lectura', color='skyblue', alpha=0.8)
            plt.bar(x_alt + width/2, promedios_alt['puntaje_matematica'], width, 
                   label='Matemática', color='lightcoral', alpha=0.8)
            
            plt.xlabel('Nivel Socioeconómico')
            plt.ylabel('Puntaje Promedio')
            plt.title('Promedio de Puntajes por Nivel Socioeconómico')
            plt.xticks(x_alt, promedios_alt.index, rotation=45)
            plt.legend()
            
        except Exception as e2:
            print(f"Error en gráfica alternativa: {e2}")
            plt.text(0.5, 0.5, 'Error generando gráfica NSE', ha='center', va='center', transform=plt.gca().transAxes)
    
    plt.tight_layout()
    plt.savefig('grafica4_nivel_socioeconomico.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Gráfica 4 guardada: grafica4_nivel_socioeconomico.png")

def grafica_5_real_vs_predicho(df):
    """Gráfica 5: Relación entre puntajes reales y predichos"""
    # Preparar datos para el modelo
    categorical_vars = ['sexo', 'lengua_materna', 'gestion', 'zona', 'nivel_socioeconomico', 'departamento']
    available_vars = [var for var in categorical_vars if var in df.columns]
    
    # Codificar variables
    df_encoded = df.copy()
    for var in available_vars:
        le = LabelEncoder()
        df_encoded[var] = le.fit_transform(df_encoded[var].astype(str))
    
    X = df_encoded[available_vars]
    y = df_encoded['puntaje_lectura']
    
    # Dividir datos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Entrenar modelo con parámetros PSO
    rf = RandomForestRegressor(n_estimators=88, max_depth=6, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    
    # Crear gráfica
    plt.figure(figsize=(10, 8))
    
    # Scatter plot
    plt.scatter(y_test, y_pred, alpha=0.6, color='skyblue', s=20)
    
    # Línea de identidad
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Línea de identidad (y=x)')
    
    # Línea de regresión
    z = np.polyfit(y_test, y_pred, 1)
    p = np.poly1d(z)
    plt.plot(y_test, p(y_test), 'g-', linewidth=2, alpha=0.8, label=f'Regresión lineal')
    
    plt.xlabel('Puntaje Real en Lectura')
    plt.ylabel('Puntaje Predicho en Lectura')
    plt.title('Relación entre Puntajes Reales y Predichos en Lectura', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Añadir R²
    r2 = r2_score(y_test, y_pred)
    plt.text(0.05, 0.95, f'R² = {r2:.4f}', transform=plt.gca().transAxes, 
             fontsize=12, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('grafico_real_vs_predicho.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Gráfica 5 guardada: grafico_real_vs_predicho.png")

def grafica_6_mapa_calor_departamentos(df):
    """Gráfica 6: Mapa de calor del rendimiento por departamentos"""
    # Calcular promedios por departamento
    dept_promedios = df.groupby('departamento')['puntaje_lectura'].mean().sort_values(ascending=False)
    
    # Crear categorías de riesgo
    q25 = dept_promedios.quantile(0.25)
    q50 = dept_promedios.quantile(0.50)
    q75 = dept_promedios.quantile(0.75)
    
    def categorizar_riesgo(puntaje):
        if puntaje >= q75:
            return 4  # Óptimo
        elif puntaje >= q50:
            return 3  # Medio
        elif puntaje >= q25:
            return 2  # Alto
        else:
            return 1  # Crítico
    
    dept_promedios_df = dept_promedios.reset_index()
    dept_promedios_df['categoria'] = dept_promedios_df['puntaje_lectura'].apply(categorizar_riesgo)
    dept_promedios_df['categoria_label'] = dept_promedios_df['categoria'].map({
        4: 'Óptimo', 3: 'Medio', 2: 'Alto', 1: 'Crítico'
    })
    
    # Crear gráfica de calor
    plt.figure(figsize=(14, 10))
    
    # Reorganizar para visualización en matriz
    n_depts = len(dept_promedios_df)
    cols = 6
    rows = (n_depts + cols - 1) // cols
    
    heatmap_data = np.zeros((rows, cols))
    labels = np.empty((rows, cols), dtype=object)
    
    for i, (_, row) in enumerate(dept_promedios_df.iterrows()):
        r, c = i // cols, i % cols
        heatmap_data[r, c] = row['categoria']
        labels[r, c] = f"{row['departamento']}\n{row['puntaje_lectura']:.1f}"
    
    # Llenar espacios vacíos
    for i in range(n_depts, rows * cols):
        r, c = i // cols, i % cols
        heatmap_data[r, c] = 0
        labels[r, c] = ""
    
    # Crear mapa de calor
    colors = ['white', '#ff4444', '#ff8800', '#ffcc00', '#44ff44']  # Crítico, Alto, Medio, Óptimo
    cmap = plt.matplotlib.colors.ListedColormap(colors[1:])
    
    im = plt.imshow(heatmap_data, cmap=cmap, vmin=1, vmax=4)
    
    # Añadir etiquetas
    for i in range(rows):
        for j in range(cols):
            if labels[i, j]:
                plt.text(j, i, labels[i, j], ha='center', va='center', 
                        fontsize=8, fontweight='bold', color='black')
    
    plt.title('Mapa de Calor: Rendimiento Académico por Departamento\n(Categorización por Niveles de Riesgo)', 
              fontsize=14, fontweight='bold', pad=20)
    
    # Leyenda
    legend_elements = [
        plt.Rectangle((0,0),1,1, facecolor='#ff4444', label='Crítico'),
        plt.Rectangle((0,0),1,1, facecolor='#ff8800', label='Alto'),
        plt.Rectangle((0,0),1,1, facecolor='#ffcc00', label='Medio'),
        plt.Rectangle((0,0),1,1, facecolor='#44ff44', label='Óptimo')
    ]
    plt.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('heatmap_rendimiento_academico.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Gráfica 6 guardada: heatmap_rendimiento_academico.png")

def grafica_7_comparacion_metodos():
    """Gráfica 7: Comparación PSO vs Optuna"""
    plt.figure(figsize=(12, 8))
    
    # Datos para la gráfica
    metodos = ['PSO', 'Optuna']
    materias = ['Lectura', 'Matemática']
    
    # R² scores
    r2_lectura = [resultados_reales['lectura']['pso']['r2_mean'], 
                  resultados_reales['lectura']['optuna']['r2_mean']]
    r2_matematica = [resultados_reales['matematica']['pso']['r2_mean'], 
                     resultados_reales['matematica']['optuna']['r2_mean']]
    
    # Número de árboles
    trees_lectura = [resultados_reales['lectura']['pso']['params']['n_estimators'],
                     resultados_reales['lectura']['optuna']['params']['n_estimators']]
    trees_matematica = [resultados_reales['matematica']['pso']['params']['n_estimators'],
                        resultados_reales['matematica']['optuna']['params']['n_estimators']]
    
    # Subplot 1: R² Comparison
    plt.subplot(2, 2, 1)
    x = np.arange(len(metodos))
    width = 0.35
    
    plt.bar(x - width/2, r2_lectura, width, label='Lectura', alpha=0.8, color='skyblue')
    plt.bar(x + width/2, r2_matematica, width, label='Matemática', alpha=0.8, color='lightcoral')
    plt.xlabel('Método')
    plt.ylabel('R² Score')
    plt.title('Comparación de R² por Método')
    plt.xticks(x, metodos)
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    
    # Añadir valores
    for i, (lec, mat) in enumerate(zip(r2_lectura, r2_matematica)):
        plt.text(i - width/2, lec + 0.005, f'{lec:.3f}', ha='center', va='bottom', fontweight='bold')
        plt.text(i + width/2, mat + 0.005, f'{mat:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # Subplot 2: Eficiencia Computacional
    plt.subplot(2, 2, 2)
    plt.bar(x - width/2, trees_lectura, width, label='Lectura', alpha=0.8, color='lightgreen')
    plt.bar(x + width/2, trees_matematica, width, label='Matemática', alpha=0.8, color='orange')
    plt.xlabel('Método')
    plt.ylabel('Número de Árboles')
    plt.title('Eficiencia Computacional')
    plt.xticks(x, metodos)
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    
    # Añadir valores
    for i, (lec, mat) in enumerate(zip(trees_lectura, trees_matematica)):
        plt.text(i - width/2, lec + 5, f'{lec}', ha='center', va='bottom', fontweight='bold')
        plt.text(i + width/2, mat + 5, f'{mat}', ha='center', va='bottom', fontweight='bold')
    
    # Subplot 3: Ratio de eficiencia
    plt.subplot(2, 2, 3)
    eficiencia_lectura = trees_lectura[1] / trees_lectura[0]  # Optuna/PSO
    eficiencia_matematica = trees_matematica[0] / trees_matematica[1]  # PSO/Optuna
    
    materias_eff = ['Lectura\n(Optuna/PSO)', 'Matemática\n(PSO/Optuna)']
    ratios = [eficiencia_lectura, eficiencia_matematica]
    colors = ['red' if r > 1 else 'green' for r in ratios]
    
    bars = plt.bar(materias_eff, ratios, color=colors, alpha=0.7)
    plt.axhline(y=1, color='black', linestyle='--', alpha=0.5, label='Línea de igualdad')
    plt.ylabel('Ratio de Árboles')
    plt.title('Ratio de Eficiencia entre Métodos')
    plt.legend()
    
    # Añadir valores
    for i, (bar, ratio) in enumerate(zip(bars, ratios)):
        plt.text(bar.get_x() + bar.get_width()/2, ratio + 0.05, f'{ratio:.1f}x', 
                ha='center', va='bottom', fontweight='bold')
    
    # Subplot 4: Resumen
    plt.subplot(2, 2, 4)
    plt.text(0.1, 0.8, 'RESUMEN COMPARATIVO', fontsize=14, fontweight='bold')
    plt.text(0.1, 0.7, f'• Lectura: PSO más eficiente ({trees_lectura[0]} vs {trees_lectura[1]} árboles)', fontsize=10)
    plt.text(0.1, 0.6, f'• Matemática: Optuna más eficiente ({trees_matematica[1]} vs {trees_matematica[0]} árboles)', fontsize=10)
    plt.text(0.1, 0.5, f'• R² prácticamente idéntico en ambas materias', fontsize=10)
    plt.text(0.1, 0.4, f'• p-values > 0.05: sin diferencias significativas', fontsize=10)
    plt.text(0.1, 0.3, f'• Selección según recursos disponibles', fontsize=10, fontweight='bold')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('comparacion_metodos_completa.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Gráfica 7 guardada: comparacion_metodos_completa.png")

def generar_todas_las_graficas():
    """Función principal que genera todas las gráficas"""
    print("🎨 GENERANDO TODAS LAS GRÁFICAS PARA TU PAPER...")
    print("="*60)
    
    try:
        # Cargar datos
        df = cargar_y_preparar_datos()
        print(f"✅ Datos cargados: {len(df)} registros")
        
        # Mostrar información de las variables categóricas
        print("\n📋 Información de variables categóricas:")
        categorical_vars = ['sexo', 'zona', 'nivel_socioeconomico', 'departamento']
        for var in categorical_vars:
            if var in df.columns:
                print(f"  {var}: {df[var].unique()[:5]}...")  # Primeros 5 valores
        
        # Generar cada gráfica con manejo de errores individual
        print("\n📊 Generando gráficas...")
        
        try:
            grafica_1_distribucion_puntajes(df)
        except Exception as e:
            print(f"❌ Error en gráfica 1: {e}")
        
        try:
            grafica_2_sexo(df)
        except Exception as e:
            print(f"❌ Error en gráfica 2: {e}")
        
        try:
            grafica_3_zona(df)
        except Exception as e:
            print(f"❌ Error en gráfica 3: {e}")
            
        try:
            grafica_4_nivel_socioeconomico(df)
        except Exception as e:
            print(f"❌ Error en gráfica 4: {e}")
            
        try:
            grafica_5_real_vs_predicho(df)
        except Exception as e:
            print(f"❌ Error en gráfica 5: {e}")
            
        try:
            grafica_6_mapa_calor_departamentos(df)
        except Exception as e:
            print(f"❌ Error en gráfica 6: {e}")
            
        try:
            grafica_7_comparacion_metodos()
        except Exception as e:
            print(f"❌ Error en gráfica 7: {e}")
        
        print("\n🎉 PROCESO DE GENERACIÓN COMPLETADO!")
        print("="*60)
        print("💡 Revisa las gráficas generadas exitosamente")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        print("Verifica que el archivo Excel esté en la ruta correcta")
        print("Ruta esperada: C:/beatrizumiña/metodo-de-optimizacion/Tarea_15_Unit2/articulo_cientifico/dataset_limpio_final.xlsx")

# EJECUTAR
if __name__ == "__main__":
    generar_todas_las_graficas()